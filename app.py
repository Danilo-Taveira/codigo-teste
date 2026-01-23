import google.generativeai as genai
import time
import sys

API_KEY = "AIzaSyDDsYbyay03fsy0kwSb7LDYXQlOBUgCHzg"

genai.configure(api_key=API_KEY)

model_name = 'gemini-2.5-flash'

generation_config = {
  "temperature": 0.0,
  "top_p": 0.95,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

system_instruction = (
    "Você é um especialista sênior em Agronomia e avaliador técnico. "
    "Sua tarefa é analisar respostas sobre o cultivo de soja. "
    "Você receberá uma PERGUNTA, uma RESPOSTA DE REFERÊNCIA (Gabarito) e uma RESPOSTA CANDIDATA. "
    "Compare a candidata com a referência. "
    "Classifique a resposta candidata estritamente como: 'Incorreta', 'Mediana' ou 'Excelente'. "
    "Justifique brevemente sua classificação."
)

model = genai.GenerativeModel(
  model_name=model_name,
  generation_config=generation_config,
  system_instruction=system_instruction
)

def gerar_com_retry(prompt, max_tentativas=10):
    for tentativa in range(max_tentativas):
        try:
            return model.generate_content(prompt).text.strip()
        except Exception as e:
            erro_str = str(e)
            if "429" in erro_str or "quota" in erro_str.lower():
                tempo_espera = 60 
                print(f"\n   [!] Cota excedida (Erro 429). Aguardando {tempo_espera}s para tentar novamente...")
                
                # Barra de progresso visual
                for i in range(tempo_espera, 0, -1):
                    sys.stdout.write(f"\r   ...Retomando em {i}s ")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\r   ...Tentando novamente agora!          ")
            else:
                print(f"   ERRO IRRECUPERÁVEL: {e}")
                return "ERRO_API"
    return "FALHA_APOS_RETRIES"

# --- DADOS DA PLANILHA ---
dados_teste = [
    {
        'id': 1,
        'pergunta': 'Qual é a origem da soja?',
        'referencia': 'A soja é originária da Ásia, mais provavelmente do nordeste da China, onde surgiu como uma planta rasteira, muito distinta da soja comercial que cultivamos hoje. Sua evolução iniciou-se, aparentemente, a partir de plantas oriundas de cruzamentos naturais entre duas espécies de soja selvagem, cujo produto foi domesticado e melhorado por cientistas da antiga China.',
        'testes': {
            'Incorreta': 'A soja é uma planta nativa do Brasil, especificamente da região amazônica, onde foi descoberta pelos portugueses.',
            'Mediana': 'A soja vem da Ásia e é cultivada há muito tempo em vários países do oriente.',
            'Especialista': 'A soja (Glycine max (L.) Merrill) tem seu centro de origem e domesticação na China (região do Rio Yangtse), datando de aproximadamente 1.100 a.C. Evolutivamente, deriva da espécie selvagem Glycine soja (uma planta rasteira e volúvel), tendo sido geneticamente selecionada ao longo de milênios para hábito de crescimento ereto, indeiscência de vagens e maiores teores de proteína e óleo.'
        }
    },
    {
        'id': 2,
        'pergunta': 'Quais são as características morfológicas básicas de uma planta de soja?',
        'referencia': 'Apesar de existir variabilidade genética e influência do ambiente sobre a morfologia das plantas de soja, há características comuns ou variáveis apenas dentro de determinados limites na espécie. O sistema radicular é classificado como difuso, com um eixo principal que se ramifica.',
        'testes': {
            'Incorreta': 'A soja é uma gramínea com raízes fasciculadas superficiais e folhas longas e estreitas, parecida com o milho.',
            'Mediana': 'A planta da soja tem raízes, caule, folhas, flores e vagens. As raízes crescem para baixo e se espalham.',
            'Especialista': 'A soja (dicotiledônea) possui sistema radicular pivotante, embora a raiz principal perca dominância com o tempo, tornando-se difuso. Apresenta nódulos de Bradyrhizobium para FBN. O caule é herbáceo, pubescente, com ramificações. As folhas são alternas e trifolioladas (exceto as primárias unifolioladas). As flores são papilionáceas, autógamas, originando vagens (frutos) com 2 a 4 sementes.'
        }
    },
    {
        'id': 3,
        'pergunta': 'Como ocorre a germinação da semente de soja?',
        'referencia': 'A semente de soja, para germinar, absorve água do solo, num processo denominado embebição; em condições adequadas de umidade e temperatura, a semente incha e rompe o tegumento. Primeiro, emerge a radícula, que se fixa ao solo e, posteriormente, a região do caulículo, compreendida entre a radícula e os cotilédones, denominada hipocótilo, alonga-se, projetando os cotilédones para fora do solo.',
        'testes': {
            'Incorreta': 'A semente precisa ser plantada em solo seco e no escuro total para que a casca derreta e a planta saia.',
            'Mediana': 'A semente puxa água da terra, incha e a raiz sai primeiro, depois empurra as folhas para cima.',
            'Especialista': 'O processo é epígeo. Inicia-se com a embebição (absorção de 50% do peso em água). A radícula rompe o tegumento via micrópila. Ocorre o alongamento do hipocótilo, formando uma alça ("gancho") que rompe a superfície do solo, arrastando os cotilédones para cima (emergência). A exposição à luz induz a abertura dos cotilédones e o desenvolvimento do epicótilo.'
        }
    },
    {
        'id': 4,
        'pergunta': 'O que caracteriza o estádio vegetativo na soja?',
        'referencia': 'A fase vegetativa compreende o período desde a emergência da plântula até o aparecimento das primeiras flores (florescimento).',
        'testes': {
            'Incorreta': 'É quando a soja seca e está pronta para colher, ficando marrom.',
            'Mediana': 'É a fase em que a planta só cresce folhas e tamanho, antes de dar flor.',
            'Especialista': 'Os estádios vegetativos (V) iniciam-se na emergência (VE). Segue-se VC (cotilédones abertos), V1 (primeiro nó com folhas unifolioladas desenvolvidas) e Vn (n-ésimo nó com folha trifoliolada aberta). Caracteriza-se pelo acúmulo de biomassa, desenvolvimento radicular e fechamento do dossel, cessando ou diminuindo drasticamente (em determinadas) no início do reprodutivo (R1).'
        }
    },
    {
        'id': 5,
        'pergunta': 'Quais são os principais componentes que determinam o rendimento da soja?',
        'referencia': 'O rendimento de grãos da soja é determinado, principalmente, pelo número de plantas por área, pelo número de vagens por planta, pelo número de grãos por vagem e pelo peso dos grãos.',
        'testes': {
            'Incorreta': 'O rendimento depende apenas da quantidade de chuva e da sorte do produtor, não dá para controlar.',
            'Mediana': 'Depende de quantas plantas nascem, quantas vagens cada uma dá e o tamanho do grão no final.',
            'Especialista': 'Os componentes de rendimento são construídos sequencialmente: 1) Número de plantas/ha (definido na semeadura/emergência); 2) Número de vagens/planta (definido entre R1 e R5, influenciado por ramificações e abortamento); 3) Número de grãos/vagem (R5-R6); e 4) Peso de 1.000 grãos (enchimento em R6-R7, dependente de fotossíntese e translocação).'
        }
    },
    {
        'id': 6,
        'pergunta': 'Qual é a temperatura ideal para o desenvolvimento da soja?',
        'referencia': 'A soja adapta-se melhor a temperaturas do ar entre 20ºC e 30ºC; a temperatura ideal para seu crescimento e desenvolvimento está em torno de 30ºC.',
        'testes': {
            'Incorreta': 'A soja gosta de frio intenso, crescendo melhor abaixo de 10 graus, igual ao trigo de inverno.',
            'Mediana': 'A soja prefere temperaturas quentes, nem muito frio nem calor extremo, algo perto dos 25 ou 30 graus.',
            'Especialista': 'A temperatura base inferior é 10ºC e a superior 40ºC. A faixa ótima situa-se entre 20ºC e 30ºC. Temperaturas <= 10ºC inibem o crescimento. Na floração, temperaturas > 35ºC podem causar abortamento de flores e vagens (estresse térmico), enquanto no enchimento de grãos aceleram a senescência e reduzem o peso final.'
        }
    },
    {
        'id': 7,
        'pergunta': 'Como o fotoperíodo influencia a cultura da soja?',
        'referencia': 'A soja é uma planta de dias curtos: a indução ao florescimento ocorre quando o comprimento do dia (fotoperíodo) torna-se menor que um valor crítico (fotoperíodo crítico), o qual difere entre as cultivares.',
        'testes': {
            'Incorreta': 'A luz do sol não importa para a soja, ela floresce sempre com 50 dias de vida independente do sol.',
            'Mediana': 'A soja precisa de dias mais curtos para começar a dar flor, por isso depende da época do ano e da região.',
            'Especialista': 'Sendo planta de dia curto (ou noite longa), a soja floresce quando a nictoperíodo excede um limiar crítico. Essa sensibilidade ao fotoperíodo varia com o Grupo de Maturação Relativa (GMR). Em baixas latitudes (dias curtos), cultivares de GMR alto florescem precocemente, resultando em porte baixo. A tecnologia de Período Juvenil Longo (PJL) foi crucial para adaptar a soja ao Cerrado brasileiro.'
        }
    },
    {
        'id': 8,
        'pergunta': 'Qual é a necessidade hídrica da soja durante seu ciclo?',
        'referencia': 'A necessidade de água na cultura da soja vai aumentando com o desenvolvimento da planta, atingindo o máximo durante a floração e o enchimento de grãos (7 a 8 mm/dia), decrescendo após esse período. Para a obtenção do máximo rendimento, a necessidade total de água varia entre 450 a 800 mm/ciclo.',
        'testes': {
            'Incorreta': 'A soja é como um cacto, precisa de quase nenhuma água, uns 50mm o ciclo todo é suficiente.',
            'Mediana': 'A soja precisa de bastante água, principalmente quando está dando flor e enchendo o grão. No total precisa de uns 600mm.',
            'Especialista': 'O consumo hídrico varia de 450 a 800 mm/ciclo. Fases críticas: Germinação (precisa 50% umidade na semente) e, principalmente, Floração e Enchimento de Grãos (R1-R6), onde o déficit hídrico causa abortamento e grãos chochos. O coeficiente de cultura (Kc) atinge o pico (>1.0) no fechamento do dossel reprodutivo.'
        }
    },
    {
        'id': 9,
        'pergunta': 'Como o excesso de umidade no solo afeta a soja?',
        'referencia': 'O excesso de água no solo pode prejudicar a germinação das sementes e a emergência das plantas, pois a semente necessita também de oxigênio, que passa a não estar disponível.',
        'testes': {
            'Incorreta': 'Quanto mais água melhor, a soja adora solo encharcado e cresce mais rápido se ficar alagada.',
            'Mediana': 'Muita água no solo é Incorreta porque apodrece a semente e a planta não respira direito.',
            'Especialista': 'O encharcamento (hipoxia/anoxia) compromete a respiração radicular e a FBN, pois os rizóbios são aeróbicos. Na emergência, causa apodrecimento de sementes. Em plantas adultas, leva à clorose, redução da absorção de nutrientes e, se prolongado, morte radicular. Solos compactados agravam o problema.'
        }
    },
    {
        'id': 10,
        'pergunta': 'Qual é a importância da fixação biológica de nitrogênio na soja?',
        'referencia': 'A soja é capaz de suprir sua necessidade de nitrogênio por meio da fixação biológica, realizada por bactérias do gênero Bradyrhizobium que vivem em simbiose com a planta.',
        'testes': {
            'Incorreta': 'Não é importante, o produtor tem que aplicar ureia em grande quantidade para a soja crescer, senão ela morre.',
            'Mediana': 'É muito importante porque bactérias nas raízes pegam nitrogênio do ar e dão para a planta, economizando adubo.',
            'Especialista': 'A FBN, via simbiose com estirpes elite de Bradyrhizobium (ex: japonicum, elkanii), fornece cerca de 300 kg N/ha, suprindo totalmente a demanda da cultura para altas produtividades. Isso dispensa a adubação nitrogenada mineral, reduzindo drasticamente o custo de produção e o impacto ambiental (pegada de carbono) da sojicultura brasileira.'
        }
    },
    {
        'id': 11,
        'pergunta': 'Como deve ser feita a inoculação das sementes de soja?',
        'referencia': 'A inoculação deve ser realizada à sombra, e as sementes devem ser semeadas no mesmo dia, para evitar a morte das bactérias pelo calor e pelo ressecamento.',
        'testes': {
            'Incorreta': 'Pode misturar o inoculante no sol quente e deixar a semente guardada por uma semana antes de plantar.',
            'Mediana': 'Tem que misturar o inoculante na semente na sombra e plantar logo para o bicho não morrer.',
            'Especialista': 'A inoculação deve garantir > 1,2 milhão de células viáveis/semente. Recomenda-se uso de inoculantes turfosos ou líquidos registrados, aplicados via tratamento de sementes (TS) ou no sulco. Deve-se evitar contato direto com fungicidas tóxicos às bactérias e proteger da radiação UV e calor excessivo. A reinoculação anual é prática recomendada para maximizar a eficiência.'
        }
    },
    {
        'id': 12,
        'pergunta': 'O que é a coinoculação na cultura da soja?',
        'referencia': 'A coinoculação consiste no uso conjunto de Bradyrhizobium (fixação de nitrogênio) e Azospirillum (promoção de crescimento), potencializando o desenvolvimento radicular e a nutrição da planta.',
        'testes': {
            'Incorreta': 'É quando se planta soja e milho juntos no mesmo buraco para economizar espaço.',
            'Mediana': 'É usar dois tipos de bactérias, uma para o nitrogênio e outra para a raiz crescer mais.',
            'Especialista': 'Técnica que associa bactérias fixadoras de N (Bradyrhizobium) com bactérias promotoras de crescimento vegetal (Azospirillum brasilense). O Azospirillum produz fitohormônios (auxinas) que incrementam a biomassa radicular, aumentando a área de exploração do solo e a absorção de água e nutrientes, resultando em ganhos médios de produtividade de 16% (Embrapa).'
        }
    },
    {
        'id': 13,
        'pergunta': 'Quais são os principais micronutrientes exigidos pela soja?',
        'referencia': 'Os micronutrientes mais importantes para a soja, especialmente em solos de cerrados, são o zinco, o boro, o cobre e o manganês, além do molibdênio e do cobalto, essenciais para a fixação biológica do nitrogênio.',
        'testes': {
            'Incorreta': 'A soja só precisa de NPK (Nitrogênio, Fósforo e Potássio), o resto já tem na terra e não faz falta.',
            'Mediana': 'Precisa de zinco, boro, manganês e também de cobalto e molibdênio para as bactérias funcionarem.',
            'Especialista': 'Além de Mn, Zn, Cu, B e Fe, a soja demanda especificamente Cobalto (Co) e Molibdênio (Mo). O Mo é cofator da enzima nitrogenase e o Co é essencial para a síntese de leghemoglobina nos nódulos. A deficiência destes compromete severamente a FBN. O Manganês (Mn) também é crítico, especialmente em solos com calagem excessiva (pH alto) ou aplicação de Glyphosate.'
        }
    },
    {
        'id': 14,
        'pergunta': 'Quais são as principais pragas que atacam a parte aérea da soja?',
        'referencia': 'Entre as pragas que atacam a parte aérea, destacam-se as lagartas desfolhadoras (como a lagarta-da-soja e a falsa-medideira) e os percevejos sugadores de grãos (como o percevejo-marrom e o percevejo-verde-pequeno).',
        'testes': {
            'Incorreta': 'As principais pragas são pulgas e carrapatos que sugam o sangue da planta.',
            'Mediana': 'As piores são as lagartas que comem as folhas e os percevejos que furam o grão.',
            'Especialista': 'O complexo de lagartas (Anticarsia gemmatalis, Chrysodeixis includens, Spodoptera spp., Helicoverpa armigera) causa desfolha e danos reprodutivos. O complexo de percevejos (Euschistus heros, Piezodorus guildinii, Nezara viridula) é crítico na fase reprodutiva (R3-R7), causando abortamento, grãos picados, retenção foliar ("soja louca") e perda de qualidade fisiológica da semente.'
        }
    },
    {
        'id': 15,
        'pergunta': 'Qual é a estratégia do Manejo Integrado de Pragas (MIP) na soja?',
        'referencia': 'O MIP preconiza o uso racional de inseticidas, aplicando-os apenas quando a população de pragas atinge níveis de dano econômico, preservando os inimigos naturais e reduzindo custos e impactos ambientais.',
        'testes': {
            'Incorreta': 'MIP é passar veneno toda semana preventivamente para não deixar nenhum bicho aparecer na lavoura.',
            'Mediana': 'É monitorar a lavoura e só aplicar remédio quando a quantidade de praga for perigosa, para não matar os bichos bons.',
            'Especialista': 'O MIP-Soja baseia-se no monitoramento frequente (pano de batida) para tomada de decisão baseada em Níveis de Ação (ex: 2 percevejos/m em grãos). Prioriza o controle biológico, uso de cultivares resistentes (ex: Bt) e inseticidas seletivos. Busca manter as pragas abaixo do Nível de Dano Econômico (NDE), integrando táticas para sustentabilidade do sistema.'
        }
    },
    {
        'id': 16,
        'pergunta': 'O que é a ferrugem-asiática da soja e qual sua importância?',
        'referencia': 'A ferrugem-asiática, causada pelo fungo Phakopsora pachyrhizi, é a doença mais severa da cultura. Ela causa desfolha precoce, impedindo a completa formação dos grãos e reduzindo drasticamente a produtividade se não controlada.',
        'testes': {
            'Incorreta': 'É uma doença causada por um vírus que deixa a folha azul e não afeta muito a produção.',
            'Mediana': 'É um fungo muito forte que faz as folhas caírem cedo e dá muito prejuízo se não passar fungicida.',
            'Especialista': 'Causada pelo fungo biotrófico Phakopsora pachyrhizi, dissemina-se pelo vento (uredosporos). Sintomas iniciam no baixeiro. Causa desfolha prematura severa, encurtando o ciclo e impedindo o enchimento de grãos (redução do peso de grãos). Exige monitoramento, vazio sanitário e aplicações preventivas de fungicidas (sítio-específicos + multissítios) para controle.'
        }
    },
    {
        'id': 17,
        'pergunta': 'Como o plantio direto beneficia o cultivo da soja?',
        'referencia': 'O plantio direto protege o solo contra a erosão, mantém a umidade, aumenta a matéria orgânica e melhora a atividade biológica do solo, resultando em maior estabilidade produtiva.',
        'testes': {
            'Incorreta': 'O plantio direto é Incorreta porque o solo fica duro e as raízes não entram, tem que arar todo ano.',
            'Mediana': 'Ajuda a segurar a água na terra, evita erosão e deixa o solo mais forte com as palhadas.',
            'Especialista': 'O Sistema Plantio Direto (SPD) baseia-se em: não revolvimento do solo, cobertura permanente (palhada) e rotação de culturas. Beneficia a soja por reduzir erosão laminar, aumentar infiltração e retenção de água (menor estresse em veranicos), incrementar Matéria Orgânica (MOS) e CEC, além de reduzir a temperatura do solo na semeadura.'
        }
    },
    {
        'id': 18,
        'pergunta': 'Qual a diferença entre soja convencional e soja orgânica?',
        'referencia': 'A soja convencional utiliza tecnologias modernas como fertilizantes químicos e agrotóxicos para controle de pragas e doenças. Já a soja orgânica é cultivada sem o uso de produtos químicos sintéticos ou organismos geneticamente modificados, focando em práticas sustentáveis e biológicas.',
        'testes': {
            'Incorreta': 'Não tem diferença nenhuma, é tudo o mesmo grão, só muda o preço que cobram no mercado.',
            'Mediana': 'A convencional usa adubo químico e veneno. A orgânica não usa química pesada e é mais natural.',
            'Especialista': 'O manejo convencional utiliza fertilizantes minerais solúveis, sementes transgênicas (maioria) e defensivos químicos para proteção. O manejo orgânico (Lei 10.831) exige certificação e rastreabilidade. O manejo exclui OGM (Organismos Geneticamente Modificados), fertilizantes de alta solubilidade e agrotóxicos sintéticos. Baseia-se em controle biológico, adubação verde, compostagem e pós de rocha, atendendo a nichos de mercado que pagam ágios significativos sobre a commodity convencional.'
        }
    },
    {
        'id': 19,
        'pergunta': 'Qual é a importância da soja entre as grandes explorações agrícolas mundiais?',
        'referencia': 'A soja é a principal oleaginosa anual produzida e consumida no mundo. A importância do produto se dá tanto para o consumo animal, com o farelo da soja, quanto para o consumo humano, principalmente por meio do óleo. Em 2017, as exportações do complexo agroindustrial da soja somaram US$ 31,7 bilhões, valor que corresponde a 33% do total exportado pelo agronegócio (US$ 96,0 bilhões). As exportações de grãos, farelo e óleo de soja alcançaram, respectivamente, US$ 25,712 bilhões, US$ 4,973 bilhões e US$ 1,013 bilhão.',
        'testes': {
            'Incorreta': 'É uma cultura de subsistência familiar, pouco relevante no mercado internacional se comparada ao trigo e arroz.',
            'Mediana': 'É a cultura mais importante do Brasil, gera muito dinheiro com exportação para a China e move o agronegócio.',
            'Especialista': 'Economicamentente, a soja é a "commodity" agrícola mais líquida e transacionada globalmente, com formação de preço na Bolsa de Chicago (CBOT). Representa a base do superávit comercial brasileiro e argentino. Sua cadeia produtiva move indústrias de insumos, maquinário, logística e processamento, sendo pilar fundamental para a segurança alimentar global como fonte proteica para ração animal (farelo) e óleo comestível/biocombustível.'
        }
    }
]


def avaliar_item_unico(item):
    id_pgt = item['id']
    pgt = item['pergunta']
    ref = item['referencia']
    
    print(f"\n" + "="*60)
    print(f"AVALIANDO PERGUNTA ID {id_pgt}: {pgt}")
    print("="*60)
    
    for tipo, resposta_candidata in item['testes'].items():
        
        prompt_juiz = (
            f"PERGUNTA: {pgt}\n\n"
            f"RESPOSTA REFERÊNCIA (GABARITO): {ref}\n\n"
            f"RESPOSTA CANDIDATA ({tipo} - Ignore o rótulo, avalie o conteúdo): {resposta_candidata}\n"
        )
        
        print(f"\n>> Analisando resposta '{tipo}'...")
        avaliacao = gerar_com_retry(prompt_juiz)
        
        print(f"   RESULTADO: {avaliacao}")
        print("-" * 30)
        
        # --- ADICIONE ISTO AQUI ---
        # Pausa de 4 segundos entre as análises das respostas da MESMA pergunta.
        # Isso garante que você nunca ultrapasse 15 RPM (60s / 4s = 15 reqs).
        time.sleep(4)


if __name__ == "__main__":
    print(f"Iniciando sistema de avaliação com modelo: {model_name}")
    
    while True:
        try:
            entrada = input("\nDigite o número da pergunta para avaliar (1-19) ou 0 para Sair: ").strip()
            
            if not entrada.isdigit():
                print("Por favor, digite apenas números.")
                continue
            
            escolha = int(entrada)
            
            if escolha == 0:
                print("Encerrando...")
                break
            
            # Busca a pergunta pelo ID
            item_selecionado = next((item for item in dados_teste if item['id'] == escolha), None)
            
            if item_selecionado:
                avaliar_item_unico(item_selecionado)
            else:
                print(f"Erro: Pergunta ID {escolha} não encontrada. Tente entre 1 e 19.")
                
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")