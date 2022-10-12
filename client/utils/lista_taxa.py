from utils.operar import Operacao
import threading, time

class ListaTaxa(Operacao):
    def verificar_tendencia(self, paridade, direcao, timeframe):
        tendecia = self.config.get('tendencia', False)
        if (tendecia and not self.calcular_tendencia(paridade, 
            direcao, timeframe, self.config['periodo_tendencia'])):
            self.mostrar_mensagem(
                f"[❗️] {paridade}|{direcao.upper()} está contra a tendência. [❗️]")
            return True
        return False

    def operar_lista_taxas(self):
        '''
        1 - Percorre todos os comandos.
        2 - Pausa o script até a próxima hora:min
        3 - Calcula o payout da paridade
        4 - Cria uma thread para o método operar
        '''
        def formatHour(number):
            '''
            Converte números de 1 dígito para 2 dígitos:
                0:0 -> 00:00
                2/1/2000 -> 02/01/2000
            '''
            return str(number) if len(str(number)) != 1 else "0" + str(number)

        par_taxa = {}  
        if len(self.espera) > 0:
            self.stop_wait_list = True
            for thread in self.espera:
                thread.join()
            self.stop_wait_list = False
        
        self.espera = []
        for comando in self.comandos:
            if comando["tipo"] == "taxas":
                paridade = comando['par']
                valor = (comando['taxa'], comando['timeframe'])
                if paridade not in par_taxa:
                    par_taxa[paridade] = [valor]
                else:
                    par_taxa[paridade].append(valor)
        
        for paridade, taxas in par_taxa.items():
            thread = threading.Thread(
                target = self.esperar_taxa, 
                name = f"{time.time()}", 
                args = (paridade, taxas),
                daemon = True)
            self.espera.append(thread)
            thread.start()

        self.comando_atual = 0
        self.comandos.sort(key = lambda x: x["timestamp"])
        if len(self.comandos) == 0:
            self.mostrar_mensagem("Nenhuma lista de sinais encontrada.")
        while self.comando_atual < len(self.comandos):
            index = self.comando_atual
            comando = self.comandos[index]
            if comando["tipo"] == "taxas": 
                self.comando_atual += 1
                continue

            data = comando["data"]
            horas, minutos = comando["hora"]
            tempo = comando['timeframe']
            tempo = tempo if tempo > 0 else self.config.get("tempo", 5)
            segundos = 0

            if self.esperarAte(horas, minutos, segundos, data, 
                self.config.get('correcao', 0) + 1, True):

                valor = self.valor
                par = comando['par']
                ordem = comando['ordem']
                minimo = self.config.get("minimo", 0)
                tipo, payout = self.recebe_payout(par, tempo)

                if self.verificar_tendencia(par, ordem, tempo):
                    continue

                if self.verificar_stop():
                    break
                
                if minimo <= payout:
                    thread = threading.Thread(
                        target = self.realizar_trade, 
                        name = f"{time.time()}", 
                        args = (valor, par, ordem, tempo, payout, tipo),
                        daemon = True)
                    self.espera.append(thread)
                    thread.start()
                    self.valor = self.valor_inicial
                else:
                    self.mostrar_mensagem(f"{par} tem payout inferior: {payout}% < {minimo}%")
                remaning = len(self.comandos) - index
                self.mostrar_mensagem(f"Operando lista: {remaning} sinais restantes.")
            else:
                self.mostrar_mensagem(f" ⏰ {comando['par']} - {formatHour(horas)}:{formatHour(minutos)} passou da hora ⏰ ")
            self.comando_atual += 1

    def esperar_taxa(self, par, taxas):
        '''
        1 - Verifica se a taxa atual ultrapassou alguma das especificadas
        2 - Cria uma thread para o método operar
        '''
        ultimo = {}
        self.API.start_candles_stream(par, 60, 1)
        while ultimo == {}:
            ultimo = self.API.get_realtime_candles(par, 60)
            ultimo = ultimo[list(ultimo.keys())[0]]['close']
            time.sleep(1)

        taxa_time = lambda x: f"{x[0]} M{x[1]}".replace(
            "M0", f"M{self.config.get('tempo', 5)}")
        self.mostrar_mensagem(f"{par.upper()} esperando bater nas taxas:\n" + 
            '\n'.join(list(map(taxa_time, taxas))))
        while not self.verificar_stop() and taxas != [] and not self.stop_wait_list:
            velas = self.API.get_realtime_candles(par, 60)
            abertura = velas[list(velas.keys())[0]]['open']
            fechamento = velas[list(velas.keys())[0]]['close']

            for taxa, timeframe in taxas:
                _timeframe = self.config.get("tempo", 1) if timeframe == 0 else timeframe
                if (fechamento >= taxa and ultimo < taxa or 
                    fechamento <= taxa and ultimo > taxa):

                    direcao = "call" if abertura > fechamento else "put"
                    tipo, payout = self.recebe_payout(par, _timeframe)
                    minimo = self.config.get("minimo", 0)

                    if (self.ativar_noticias and
                        not self.verificar_noticias(par)):
                        continue

                    if minimo <= payout:
                        self.mostrar_mensagem(f"Taxas: {par} {taxa} ")

                        if self.config.get("taxas_vela", "atual") != "atual":
                            self.esperar_proximo_minuto()

                        thread = threading.Thread(
                            target = self.realizar_trade, 
                            name = f"{time.time()}", 
                            args = (self.valor, par, direcao, 
                                _timeframe, payout, tipo),
                            daemon = True)
                        self.espera.append(thread)
                        thread.start()
                    else:
                        self.mostrar_mensagem(
                            f"{par} {taxa} não atende o payout mínimo {payout}% < {minimo}%")
                    
                    try: taxas.remove((taxa, timeframe))
                    except: pass
            ultimo = fechamento
            time.sleep(self.config.get('correcao', 0))
        self.API.stop_candles_stream(par, 60)