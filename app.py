import time
import ollama

model_name = 'llama3'

system_instruction = (
    "Você é um especialista sênior em Agronomia e avaliador técnico. "
    "Sua tarefa é analisar respostas sobre o cultivo de soja. "
    "Você receberá uma PERGUNTA, uma RESPOSTA DE REFERÊNCIA (Gabarito) e uma RESPOSTA CANDIDATA. "
    "Compare a candidata com a referência. "
    "Classifique a resposta candidata estritamente como: 'Incorreta', 'Mediana' ou 'Excelente'. "
    "Justifique brevemente sua classificação."
)

def gerar_resposta_llama(prompt):
    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0.0,
                "num_ctx": 8192,     # contexto grande (importante para seu prompt longo)
                "num_predict": 2048 # limite de saída (ajuste se quiser)
            }
        )
        return response['message']['content'].strip()

    except Exception as e:
        print(f"ERRO LLaMA LOCAL: {e}")
        return "ERRO_LLM_LOCAL"

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
        'referencia': 'Apesar de existir variabilidade genética e influência do ambiente sobre a morfologia das plantas de soja, há características comuns ou variáveis apenas dentro de determinados limites na espécie. O sistema radicular é classificado como difuso, com um eixo principal que pode medir em torno de 2 m de profundidade e um grande número de raízes laterais localiza das principalmente nos primeiros 15 cm abaixo da superfície do solo. A parte aérea é constituída por uma haste principal, à qual inicialmente se conectam dois cotilédones verdes, sésseis (sem pecíolos), inseridos em um par de nós chamados cotiledonares, opostos (com posições opostas), na mesma altura da haste. Os dois cotilédones evoluem para duas folhas cotiledonares sésseis, simples, pequenas, opostas e elípticas, que com o tempo se destacam e deixam os nós cotiledonares como vestígios. A plântula (planta inicial) é predominantemente verde, mas o hipocótilo (região abaixo dos cotilédones) pode ser verde ou arroxeado em plantas que terão flores brancas ou roxas, respectivamente. Outro par de folhas também opostas, chamadas unifolioladas, é originado de primórdios foliares e se insere no ápice do epicótilo (região acima dos cotilédones), em um segundo par de nós, chamados nós unifoliolados, semelhante aos nós cotiledonares. Essas folhas unifolioladas são pecioladas (como todas as folhas acima), maiores, mais finas e posicionadas distintamente das cotiledonares. Juntamente com os nós correspondentes, elas demarcam o ápice do epicótilo, como o primeiro de vários entrenós (segmentos da haste entre dois nós). Outros nós, folhas e entrenós se sucedem, desenvolvidos a partir da gema apical, no processo de crescimento que dá origem a toda a haste. A haste, como toda a parte aérea da planta, com exceção das flores, se recobre de tricomas (pubescência) nas cores cinza ou marrom. Nos nós superiores aos unifoliolados, as folhas são trifolioladas (compostas por três folíolos) e alternas (posicionadas em nós com alturas diferentes da haste), com posicionamento na haste sempre deslocado em relação à folha inferior, a fim de permitir maior passagem de luz. Os folíolos, inicialmente cilíndricos, adquirem formato final ovado, com variações mais afiladas. Os entrenós sobrepostos variam em comprimento (inclusive dentro da planta) e número, resultando em plantas com alturas diversas, normalmente em torno de 70 cm a 150 cm. Nas axilas das folhas, se desenvolvem estruturas vegetativas (ramos) ou reprodutivas (flores), a partir de gemas axilares. Os ramos são semelhantes à haste principal, podendo inclusive ter ramos secundários inseridos em si.As flores, com 3 mm a 8 mm de diâmetro, são brancas ou roxas, agrupadas em racemos. As flores que vingam dão origem a vagens ligeiramente arqueadas, constituídas por duas valvas de um carpelo simples, com um a cinco locos. As vagens, com os locos normalmente preenchidos por sementes, têm cor inicial verde, cor final variando entre amarelo-palha, marrom e preta, e tamanho final de 2 cm a 7 cm. As sementes lisas, normalmente com certo brilho, de formato inicial elíptico e formato final oval, globoso ou elíptico, tem cor inicial verde e cor final amarela, verde, marrom ou preta. Conforme a cultivar, o hilo (região de fixação da semente na vagem) pode ter cor amarela, preta ou marrom, em vários tons. As cores claras do hilo estão ligadas à pubescência cinza da planta; e as escuras, à pubescência marrom. Cada semente pode pesar de 0,1 g a 0,2 g.',
        'testes': {
            'Incorreta': 'A soja possui raiz fasciculada idêntica à do milho, suas folhas são longas e paralelas e a produção ocorre em espigas no topo da planta.',
            'Mediana': 'É uma planta com raiz, caule, folhas verdes e vagens. As folhas caem quando a planta está pronta para colher e as vagens guardam os grãos.',
            'Especialista': 'A planta apresenta morfologia complexa regida por estádios fenológicos (Vegetativos V e Reprodutivos R). Possui sistema radicular pivotante (se não compactado), folhas cotiledonares, unifolioladas e, subsequentemente, trifolioladas alternas. O hábito de crescimento pode ser determinado (o meristema apical encerra com um racemo floral) ou indeterminado (continua crescendo após o florescimento), característica crucial para o manejo da cultura.'
        }
    },
    {
        'id': 3,
        'pergunta': 'Quais são as limitações climáticas para o cultivo da soja no Brasil?',
        'referencia': 'O cultivo da soja apresenta poucas limitações climáticas nas  áreas agricultáveis do Brasil. As limitações decorrem principalmente de irregularidade na distribuição de chuvas, que promove escassez hídrica no período de cultivo.A disponibilidade hídrica durante a estação de crescimento das plantas é a principal limitação à expressão do potencial de rendimento da cultura e a maior causa de variabilidade dos rendimentos de grãos observados de um ano para outro, principalmente no Sul do Brasil. Outro problema é o excesso de chuvas na colheita, especialmente em Mato Grosso. Há anos em que temperaturas extremas ocorridas em algumas regiões, inclusive no oeste e no norte do Paraná, também limitam o cultivo de soja. Em terras baixas de regiões tropicais, excessos de calor e umidade prejudicam a produção de sementes de soja, mas podem ser adequadas para a produção de grãos.',
        'testes': {
            'Incorreta': 'A soja é uma cultura de clima frio polar, não suportando as temperaturas tropicais do Brasil, crescendo apenas no inverno do Rio Grande do Sul.',
            'Mediana': 'O clima do Brasil é bom para soja, mas se faltar chuva ela morre. O calor excessivo também pode atrapalhar a produção.',
            'Especialista': 'A soja é uma planta termossensível e fotoperiódica (planta de dias curtos), cuja indução floral depende do comprimento da noite (escotoperíodo). Temperaturas ideais situam-se entre 20º e 30º; temperaturas acima de 40º causam abortamento floral. O déficit hídrico é crítico, demandando entre 450mm a 800mm por ciclo, com pico de consumo (7-8mm/dia) no enchimento de grãos.'
        }
    },
    {
        'id': 4,
        'pergunta': 'Qual é a classificação botânica da soja?',
        'referencia': 'A soja, que era incluída na família Leguminosae, atualmente pertence à família Fabaceae, uma das maiores famílias botânicas, com ampla distribuição pelo mundo. É a terceira maior família de plantas terrestres em número de espécies, com mais de 650 gêneros e 18 mil espécies. A soja pertence ao gênero Glycine, que se subdivide em dois subgêneros: Glycine e Soja. Dentro do subgênero Soja, existem duas espécies reconhecidas: Glycine max e Glycine soja. A soja cultivada pertence à espécie G. max.',
        'testes': {
            'Incorreta': 'Pertence à família Poaceae (gramíneas), gênero Zea, sendo da mesma família botânica do trigo e do arroz.',
            'Mediana': 'É uma leguminosa, parente do feijão, e seu nome científico é Glycine max.',
            'Especialista': 'Taxonomicamente, classifica-se na família Fabaceae (Leguminosae), subfamília Faboideae, gênero Glycine e espécie Glycine max (L.) Merrill. É uma espécie diploide, porém com genoma paleopoliploide (2n=40 cromossomos), o que confere grande plasticidade genética para programas de melhoramento focados em produtividade e resistência biótica/abiótica.'
        }
    },
    {
        'id': 5,
        'pergunta': 'O que deve ser considerado na escolha da cultivar de soja?',
        'referencia': 'O agricultor deve atentar para fatores, como: adaptação da cultivar às condições de solo e de clima da região, que vai se refletir na produtividade e na estabilidade, ciclo da cultivar, de acordo com o sistema de produção a ser empregado, resistência ou tolerância da cultivar às principais espécies de nematoides e doenças que predominam na região, se a cultivar é convencional ou transgênica.',
        'testes': {
            'Incorreta': 'A única coisa que importa é a cor da flor e o tamanho da vagem, não sendo necessário observar o clima ou o solo da região.',
            'Mediana': 'Tem que escolher a semente que produz mais sacos por hectare e que aguenta bem o veneno contra lagarta.',
            'Especialista': 'A escolha técnica deve basear-se na interação Genótipo x Ambiente (GxA). Prioriza-se o Grupo de Maturidade Relativa (GMR) adequado à janela de semeadura e latitude, o hábito de crescimento, o teto produtivo, a estabilidade fenotípica e o pacote de biotecnologia embarcado (resistência a herbicidas como glifosato/2,4-D e a lepidópteros) para o manejo fitossanitário local.'
        }
    },
    {
        'id': 6,
        'pergunta': 'O que é preparo convencional do solo?',
        'referencia': 'Trata-se de um sistema de manejo em que o solo é submetido a operações de preparo antes da semeadura, por meio de operações primárias como aração, gradagem pesada e subsolagem, seguidas de operações secundárias realizadas por meio de grades intermediárias ou leves, em operação única ou sucessiva. Todas essas operações têm por objetivo deixar o solo pronto para a realização da semeadura.',
        'testes': {
            'Incorreta': 'É o sistema de plantio direto, onde não se mexe no solo e se planta a semente diretamente sobre a palha da cultura anterior.',
            'Mediana': 'É quando o agricultor passa o arado e a grade para revirar a terra e limpar o mato antes de plantar.',
            'Especialista': 'O preparo convencional caracteriza-se pela inversão das camadas do solo via aração e gradagem, visando a descompactação mecânica e controle inicial de daninhas. Contudo, essa prática expõe o solo à erosão e oxida a matéria orgânica. Tecnicamente, é preterido em favor do Sistema de Plantio Direto (SPD), exceto em casos de correção profunda de perfil ou incorporação de calcário em áreas novas.'
        }
    },
        {
        'id': 7,
        'pergunta': 'Quais são os princípios nos quais se baseia o manejo da adubação da soja?',
        'referencia': 'O manejo da adubação da soja baseia-se no diagnóstico da fertilidade do solo, na exigência nutricional da cultura, no potencial produtivo esperado e no custo do fertilizante em relação ao produto.',
        'testes': {
            'Incorreta': 'O manejo baseia-se exclusivamente na aplicação foliar de nitrogênio, pois a soja não absorve nutrientes pelas raízes.',
            'Mediana': 'O manejo da adubação da soja baseia-se principalmente na análise do solo, na reposição dos nutrientes retirados pela cultura e na correção da fertilidade do solo. Também considera as necessidades nutricionais da planta ao longo do seu desenvolvimento, buscando garantir uma produção adequada e sustentável.',
            'Especialista': 'O manejo da adubação da soja fundamenta-se em princípios técnicos que visam garantir alta produtividade com sustentabilidade. Entre eles destacam-se a análise e interpretação do solo, que orienta a correção da acidez e a disponibilidade de nutrientes; a adubação de correção e manutenção, visando suprir e repor os nutrientes extraídos pela cultura; o respeito às exigências nutricionais da soja em cada fase de desenvolvimento; a eficiência do uso de fertilizantes, evitando desperdícios e impactos ambientais; e a fixação biológica do nitrogênio, que reduz a necessidade de adubação nitrogenada quando bem manejada. Esses princípios permitem equilíbrio nutricional, produtividade e conservação do solo.'
        }
    },
    {
        'id': 8,
        'pergunta': 'O que é fixação biológica de nitrogênio (FBN)?',
        'referencia': 'É o processo pelo qual o nitrogênio atmosférico (N2) é transformado em uma forma assimilável pelas plantas. A contribuição mais importante ocorre pela simbiose de bactérias benéficas chamadas de rizóbios, que se associam a várias espécies de leguminosas e formam nódulos nas raízes, onde ocorre a quebra da forte ligação tripla covalente do N2 e a disponibilização para a planta. A pesquisa seleciona bactérias mais eficientes para cada leguminosa, visando incrementar a contribuição para as plantas. Essas bactérias são acrescentadas ao cultivo por um insumo denominado inoculante',
        'testes': {
            'Incorreta': 'É um processo industrial onde o nitrogênio é fixado nas folhas da soja através da aplicação de inseticidas à base de amônia.',
            'Mediana': 'É quando a planta pega o nitrogênio do ar sozinha e usa para crescer, sem precisar de adubo químico nitrogenado.',
            'Especialista': 'A FBN é uma simbiose mutualística entre a soja e bactérias do gênero Bradyrhizobium (principalmente B. japonicum e B. elkanii). As bactérias colonizam as raízes formando nódulos onde a enzima nitrogenase converte o N2 atmosférico em amônia (NH3), assimilável pela planta. Tecnologias como a coinoculação com Azospirillum brasilense potencializam esse processo e o desenvolvimento radicular.'
        }
    },
    {
        'id': 9,
        'pergunta': 'Quais são os sistemas de produção de soja mais comumente utilizados no Brasil?',
        'referencia': 'Existem vários sistemas de produção de soja no Brasil. Em regiões tropicais ou com clima de transição – subtropical para tropical –, a soja vem sendo cultivada em sucessão com culturas de segunda safra, sobretudo milho, sorgo, feijão comum, girassol ou algodão. Nessas regiões, a soja também é cultivada em sistemas integrados com a pecuária, com o uso de pastagens anuais ou perenes, especialmente formadas com braquiárias, além do cultivo de milheto para cobertura do solo na entressafra da soja. Nas regiões com clima subtropical, é comum a sucessão da soja com cereais de inverno, como o trigo, além do uso de pastagens anuais com aveias e/ou azevém. No Brasil, há muitas regiões em que o regime de chuvas não permite mais de um cultivo por ano, nesses casos é comum o pousio por 6 a 7 meses na entressafra da soja. É importante mencionar que grande parte da soja cultivada no Brasil está inserida em sistemas pouco diversificados – com poucas espécies agrícolas –, o que dificulta a adequada rotação de culturas.',
        'testes': {
            'Incorreta': 'O sistema mais comum é o consórcio simultâneo com cana-de-açúcar ou o cultivo em áreas alagadas (inundação) como no arroz.',
            'Mediana': 'Geralmente planta soja no verão e milho safrinha no inverno, ou então deixa o boi pastar na área depois da colheita.',
            'Especialista': 'Predomina o Sistema de Plantio Direto (SPD) consolidado. O arranjo mais frequente é a sucessão de culturas, com a soja na safra de verão seguida pelo milho "safrinha" ou cereais de inverno (trigo/aveia) no Sul. Avançam também os sistemas de Integração Lavoura-Pecuária (ILP) e Lavoura-Pecuária-Floresta (ILPF), otimizando o uso da terra e a ciclagem de nutrientes.'
        }
    },
    {
        'id': 10,
        'pergunta': 'O que é uma semeadora? O que a distingue de uma semeadora-adubadora? Que tipo de semeadora é empregado na cultura da soja?',
        'referencia': 'Semeadora é uma máquina agrícola cuja função é colocar, no solo, os mais variados tipos de sementes, de acordo com a densidade, o espaçamento e a profundidade recomendados para o pleno desenvolvimento produtivo da cultura, de maneira que as sementes não sofram danos ao passarem pelos mecanismos dosadores e distribuidores. A semeadora-adubadora incorpora, além das funções acima citadas, a aplicação de fertilizantes, também atendendo a dosagem requerida e o posicionamento em relação à semente. Para semear soja, são empregadas semeadoras de precisão, cuja fonte de potência são tratores, aos quais são engatadas por sistema de três pontos ou de arrasto.',
        'testes': {
            'Incorreta': 'Semeadora é uma ferramenta manual antiga. A diferença é que a adubadora é um avião agrícola que joga as sementes.',
            'Mediana': 'A semeadora é a máquina de plantar. A adubadora é a que joga o adubo junto. A soja usa máquina de precisão.',
            'Especialista': 'Utilizam-se semeadoras-adubadoras de precisão, predominantemente pneumáticas (a vácuo) ou mecânicas (discos horizontais). O objetivo é garantir a "plantabilidade": distribuição longitudinal uniforme (sem falhas ou duplas), profundidade constante (3 - 5 cm) e contato solo-semente adequado para assegurar a emergência vigorosa e o estande de plantas planejado.'
        }
    },
    {
        'id': 11,
        'pergunta': 'Por que as plantas daninhas causam prejuízos à soja?',
        'referencia': 'Essas plantas causam prejuízos à soja principalmente porque competem com ela por água, luz e nutrientes, reduzindo o aproveitamento desses recursos pela cultura. Muitas vezes, as plantas daninhas também são hospedeiras de doenças e pragas e dificultam os tratos culturais e a colheita, o que pode causar perda de qualidade de grãos, além de redução de produtividade. O conjunto desses efeitos é denominado de interferência.',
        'testes': {
            'Incorreta': 'As plantas daninhas são benéficas pois protegem o solo do sol forte e mantém a umidade para a soja, aumentando a produção.',
            'Mediana': 'O mato cresce no meio da soja e atrapalha a colheitadeira, além de deixar a lavoura suja e tirar força da planta.',
            'Especialista': 'A interferência das plantas daninhas é crítica no Período Anterior à Interferência (PAI). Além da competição por recursos (água, luz, nutrientes), há o fenômeno da alelopatia e a dificuldade de colheita. O desafio atual é o manejo de espécies resistentes a herbicidas (ex: Conyza spp. e Digitaria insularis), exigindo rotação de mecanismos de ação química.'
        }
    },
    {
        'id': 12,
        'pergunta': 'O que é Manejo Integrado de Pragas da Soja (MIP-Soja)?',
        'referencia': 'O MIP-Soja é o uso integrado de diversas táticas de controle cuja finalidade é proteger a cultura da soja do ataque de pragas. O MIP está fundamentado na correta identificação das pragas; no monitoramento do nível populacional de pragas e de seus agentes de controle biológico presentes na lavoura; na capacidade da planta em tolerar o ataque de pragas; e em condições climáticas que interferem na interação das pragas com a cultura. O MIP não visa eliminar completamente as pragas presentes na lavoura, mas sim implementar medidas de controle apenas quando as pragas atingem nível populacional ou intensidade de ataque que proporcione risco de perdas economicamente representativas, ou seja, as pragas só devem ser controladas quando o custo do controle for economicamente compensatório diante de seu potencial de causar perdas. A tomada de decisão sobre a necessidade de controle é embasada no monitoramento constante da dinâmica populacional de pragas e seus agentes de controle biológico, o que requer métodos adequados de amostragem associados à correta identificação (reconhecimento), quantificação e registro desses organismos.',
        'testes': {
            'Incorreta': 'É a aplicação preventiva de inseticidas toda semana (calendário) para garantir que não haja nenhum inseto vivo na lavoura ("praga zero").',
            'Mediana': 'É um jeito de controlar as pragas usando menos veneno, só aplicando quando tem muito bicho na lavoura.',
            'Especialista': 'O MIP-Soja é uma filosofia de controle baseada em parâmetros técnicos: Nível de Dano Econômico (NDE) e Nível de Controle (NC). Prioriza o monitoramento (pano-de-batida), a preservação de inimigos naturais e o uso de inseticidas seletivos ou biológicos, rompendo com a aplicação calendarizada ("carona") que induz resistência nas pragas.'
        }
    },
    {
        'id': 13,
        'pergunta': 'Que tipo de organismos pode infectar a soja e que partes da planta podem ser atacadas?',
        'referencia': 'A soja pode ser infectada por fungos, chromistas, bactérias, vírus e nematoides. Tanto a parte aérea quanto as raízes podem ser atacadas. Bactérias e vírus incidem apenas na parte aérea. Esses organismos que causam doença em plantas são chamados de patógenos.',
        'testes': {
            'Incorreta': 'A soja só é atacada por vírus nas raízes; fungos só atacam as vagens quando já estão secas no armazém.',
            'Mediana': 'Doenças causadas por fungos e vírus que atacam as folhas, e vermes que atacam as raízes.',
            'Especialista': 'A cultura é suscetível a um complexo patológico que inclui fungos (ex: Ferrugem Asiática - Phakopsora pachyrhizi, Mancha Alvo, Antracnose), oomicetos, bactérias, vírus (ex: Mosaico Comum) e nematoides (ex: Cisto e Galhas). O controle foca em resistência genética, tratamento de sementes e aplicação preventiva de fungicidas sítio-específicos e multissítios.'
        }
    },
    {
        'id': 14,
        'pergunta': 'Como podem ser classificadas as colhedoras disponíveis no mercado de acordo com o sistema de trilha? O que são classes de colhedoras, de acordo com os fabricantes?',
        'referencia': 'As colhedoras podem ser classificadas em relação ao mecanismo de trilha e separação. Atualmente são dois tipos: com cilindro de trilha radial e saca-palhas; e com rotor axial. Colhedoras com cilindro radial são as mais comuns, normalmente são menores, já estão no mercado há algumas décadas e predominam em número até hoje. Já a tecnologia de trilha por rotor, presente em todos os fabricantes no Brasil, chegou um pouco mais tarde, e equipam as colhedoras de maior porte. Os fabricantes mundiais de colhedoras as classificam em classes, de acordo com a disponibilidade de potência em seus motores (CV ou HP). Atualmente, existem dez classes em âmbito mundial. As colhedoras mais modernas no mercado enquadram-se entre as classes quatro e dez (IV e X), em ordem crescente de potência.',
        'testes': {
            'Incorreta': 'As colhedoras são classificadas pela cor da lataria. O sistema de trilha é manual, feito por pessoas dentro da máquina.',
            'Mediana': 'Existem colheitadeiras convencionais e as axiais (rotor). As classes dividem as máquinas por tamanho, das pequenas às gigantes.',
            'Especialista': 'As colhedoras modernas dividem-se em sistemas de fluxo tangencial (cilindro e batedor) e fluxo axial (rotor). O sistema axial é superior na preservação da qualidade física do grão (menos quebra mecânica) e maior capacidade operacional. A classificação por "Classes" segue padrões da ASABE baseados na potência do motor, variando hoje até a Classe X (acima de 600 cv).'
        }
    },
    {
        'id': 15,
        'pergunta': 'Qual é a diferença entre sementes e grãos?',
        'referencia': 'A semente atende a padrões mínimos de qualidade e destina-se à reprodução/multiplicação, ou seja, tem como finalidade a semeadura, enquanto o grão se destina ao processamento ou consumo in natura. De acordo com a Lei de Sementes (Brasil, 2003), entende-se por “semente”: material de reprodução vegetal de qualquer gênero, espécie ou cultivar, proveniente de reprodução sexuada ou assexuada, que tenha finalidade específica de semeadura.',
        'testes': {
            'Incorreta': 'Sementes são os grãos quebrados e sujos que sobram; Grãos são os puros selecionados para o plantio.',
            'Mediana': 'Semente a gente compra caro para plantar. Grão é o que a gente colhe e vende para o armazém ou cooperativa.',
            'Especialista': 'A distinção é fisiológica e legal. "Semente" possui garantia de atributos genéticos (pureza varietal), físicos (pureza física), fisiológicos (alto vigor e germinação) e sanitários, sendo produzida sob normas estritas do Renasem (Registro Nacional de Sementes e Mudas). "Grão" é o produto comercial (commodity) destinado ao processamento industrial ou alimentação, sem requisitos de viabilidade reprodutiva.'
        }
    },
    {
        'id': 16,
        'pergunta': 'Qual é a composição do grão de soja?',
        'referencia': 'A soja destaca-se pelo seu valor nutricional, pois contém proteínas, algumas vitaminas e minerais em quantidades superiores a outros grãos. Em média, a soja possui de 35% a 38% de proteínas, 18% a 21% de lipídios (óleo), 5% a 6% de minerais e em torno de 34% de carboidratos (açúcares como glicose, frutose e sacarose, fibras e oligossacarídeos como rafinose e estaquiose). O grão de soja não contém amido.',
        'testes': {
            'Incorreta': 'É composto 80% por amido (igual ao milho) e possui baixíssimo teor de proteína e óleo.',
            'Mediana': 'Tem bastante proteína e óleo, por isso serve para fazer ração e óleo de cozinha. Também tem carboidrato.',
            'Especialista': 'O grão é uma fonte proteico-energética, composto em média por 36-40% de proteína bruta (rica em lisina e triptofano) e 18-22% de lipídios (óleo). Contém ainda carboidratos estruturais e solúveis, minerais (Ca, P, Fe) e fatores antinutricionais (inibidores de tripsina e hemaglutininas) que exigem tratamento térmico para inativação antes do consumo por monogástricos.'
        }
    },
    {
        'id': 17,
        'pergunta': 'Quais são os principais produtos oriundos da soja?',
        'referencia': 'Apesar de a soja ser a matéria-prima para a fabricação de centenas de produtos, em termos de volume, os dois mais expressivos são o farelo e o óleo. Entretanto, inúmeros outros derivados da soja são produzidos, tais como: lecitina de soja; extrato solúvel de soja, utilizado na fabricação das bebidas à base de soja (BBS); farinha de soja; concentrado proteico de soja; isolado proteico de soja; e proteína texturizada de soja.',
        'testes': {
            'Incorreta': 'O principal produto é o etanol de soja e o açúcar cristal extraído do grão.',
            'Mediana': 'Os principais são o farelo para os animais e o óleo de soja que usamos em casa.',
            'Especialista': 'O processamento industrial (esmagamento) gera dois produtos primários: o farelo de soja (sólido), base da nutrição animal mundial devido ao alto teor proteico (44 - 48%), e o óleo de soja bruto (líquido), refinado para consumo humano ou transesterificado para produção de biodiesel. Derivados incluem lecitinas, isolados proteicos e casca peletizada.'
        }
    },
    {
        'id': 18,
        'pergunta': 'O que é soja orgânica?',
        'referencia': 'É a soja cultivada em sistema orgânico de produção. No Brasil, a Lei nº 10.831, de 23 de dezembro de 2003 (Brasil, 2003), do Ministério da Agricultura, Pecuária e Abastecimento (Mapa), define o que é o sistema orgânico, mas de forma simplificada. A soja orgânica não pode ser transgênica. Além disso, não podem ser utilizados agrotóxicos nem adubos solúveis no seu cultivo e só podem ser usados insumos e práticas permitidos pela legislação de orgânicos e/ou pela certificadora.',
        'testes': {
            'Incorreta': 'É qualquer soja transgênica que não recebeu inseticida na última semana antes da colheita.',
            'Mediana': 'É a soja plantada sem veneno químico e sem adubo químico, que é vendida mais caro por ser natural.',
            'Especialista': 'A soja orgânica exige certificação auditada e rastreabilidade total. O manejo exclui OGM (Organismos Geneticamente Modificados), fertilizantes de alta solubilidade e agrotóxicos sintéticos. Baseia-se em controle biológico, adubação verde, compostagem e pós de rocha, atendendo a nichos de mercado que pagam ágios significativos sobre a commodity convencional.'
        }
    },
    {
        'id': 19,
        'pergunta': 'Qual é a importância da soja entre as grandes explorações agrícolas mundiais?',
        'referencia': 'A soja é a principal oleaginosa anual produzida e consumida no mundo. A importância do produto se dá tanto para o consumo animal, com o farelo da soja, quanto para o consumo humano, principalmente por meio do óleo. Em 2017, as exportações do complexo agroindustrial da soja somaram US$ 31,7 bilhões, valor que corresponde a 33% do total exportado pelo agronegócio (US$ 96,0 bilhões). As exportações de grãos, farelo e óleo de soja alcançaram, respectivamente, US$ 25,712 bilhões, US$ 4,973 bilhões e US$ 1,013 bilhão.',
        'testes': {
            'Incorreta': 'É uma cultura de subsistência familiar, pouco relevante no mercado internacional se comparada ao trigo e arroz.',
            'Mediana': 'É a cultura mais importante do Brasil, gera muito dinheiro com exportação para a China e move o agronegócio.',
            'Especialista': 'Economicamentente, a soja é a "commodity" agrícola mais líquida e transacionada globalmente, com formação de preço na Bolsa de Chicago (CBOT). Representa a base do superávit comercial brasileiro e argentino. Sua cadeia produtiva move indústrias de insumos, maquinário, logística e processamento, sendo pilar fundamental do PIB do agronegócio nas Américas.'
        }
    },


    
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
        avaliacao = gerar_resposta_llama(prompt_juiz)
        
        print(f"   RESULTADO: {avaliacao}")
        print("-" * 30)
        
        time.sleep(4)


if __name__ == "__main__":
    print(f"Iniciando sistema de avaliação com o modelo: {model_name}")
    
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