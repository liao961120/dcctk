Stats
================


.. container:: cell markdown

.. container:: cell code

   .. code:: python

      !gdown https://github.com/liao961120/hctk/raw/main/test/data.zip
      !unzip -q data.zip
      !pip install -qU hctk

   .. container:: output stream stdout

      ::

         Downloading...
         From: https://github.com/liao961120/hctk/raw/main/test/data.zip
         To: /content/data.zip
         100% 11.5M/11.5M [00:00<00:00, 70.2MB/s]
         ents to build wheel ... etadata ... 

.. container:: cell markdown

   .. rubric:: 1 Dispersion
      :name: 1-dispersion

.. container:: cell code

   .. code:: python

      from pprint import pprint
      from hctk import PlainTextReader, Dispersion

      dp = Dispersion(PlainTextReader("data").corpus)

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"6edf85bb5c074d658d5b95482ec8e353"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"ee96a5c61b2e4f69a823d8371933afe4"}

.. container:: cell markdown

   .. rubric:: 1.1 Dispersion Measures of Characters
      :name: 11-dispersion-measures-of-characters

.. container:: cell code

   .. code:: python

      for ch in '之也水火':
          print(ch)
          pprint(dp.char_dispersion(char=ch))

   .. container:: output stream stdout

      ::

         之
         {'DP': 0.20221115044151497,
          'DPnorm': 0.2022113683260698,
          'JuillandD': 0.9852586807096999,
          'KLdivergence': 0.19438584134276882,
          'Range': 1845,
          'RosengrenS': 0.9263264076180923}
         也
         {'DP': 0.35839650852771193,
          'DPnorm': 0.35839689470356595,
          'JuillandD': 0.9762985043690171,
          'KLdivergence': 0.5790626716815067,
          'Range': 1657,
          'RosengrenS': 0.8017462266655788}
         水
         {'DP': 0.4248753877868117,
          'DPnorm': 0.4248758455943289,
          'JuillandD': 0.9419817581882376,
          'KLdivergence': 1.2093306326342055,
          'Range': 1032,
          'RosengrenS': 0.6599676413503003}
         火
         {'DP': 0.5258856218700372,
          'DPnorm': 0.5258861885171008,
          'JuillandD': 0.9082169168517871,
          'KLdivergence': 1.5125799798374882,
          'Range': 630,
          'RosengrenS': 0.5227475458444708}

.. container:: cell markdown

   .. rubric:: 1.2 Dispersion Measures of Complex Forms (defined by CQL)
      :name: 12-dispersion-measures-of-complex-forms-defined-by-cql

.. container:: cell code

   .. code:: python

      import pandas as pd
      from hctk import Concordancer

      c = Concordancer(PlainTextReader("data").corpus)
      cql = """
      [compo="氵" & idc="horz2" & pos="0"] [compo="氵" & idc="horz2" & pos="0"]
      """.strip()
      results = list(c.cql_search(cql, left=5, right=5))

      print('Num of results:', len(results))
      for r in results[:5]: print(r)

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"231c8e09bef640c5965d4bc5e293b65c"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"9bbbfb3fb87946afa4b8bb655c54f8fa"}

   .. container:: output stream stdout

      ::

         Num of results: 9782
         <Concord 其中軍銜枚{潛涉}，不鼓不譟>
         <Concord 也？《春秋{潛潭}巴》曰：「>
         <Concord 舟之魚不居{潛澤}，度量之士>
         <Concord 色親也。』{潛潭}巴曰：『虹>
         <Concord 之厚德也。{潛潭}巴曰：『有>

.. container:: cell code

   .. code:: python

      # Compute separate dispersion measures for each subcorpus (time-sliced)
      df = []
      for i in range(dp.num_of_subcorp):
          stats, data = dp.pattern_dispersion(data=results, subcorp_idx=i, return_raw=True)
          stats['time'] = i
          stats['freq'] = data['f']
          stats['range (%)'] = stats['Range'] / data['n']
          stats['num_of_texts'] = data['n']
          stats['corpus_size'] = data['corpus_size']
          df.append(stats)

      pd.DataFrame(df)

   .. container:: output execute_result

      ::

            Range        DP    DPnorm  ...  range (%)  num_of_texts  corpus_size
         0    346  0.464641  0.464645  ...   0.472678           732      1858228
         1    621  0.276959  0.276960  ...   0.591992          1049      3938310
         2    130  0.181770  0.181792  ...   0.833333           156      2097273
         3      2  0.127389  0.235377  ...   1.000000             2       458738
         4      0  0.000000  0.000000  ...   0.000000             5           50

         [5 rows x 11 columns]

.. container:: cell markdown

   .. rubric:: 2 Hanzi Component
      :name: 2-hanzi-component

.. container:: cell code

   .. code:: python

      from hctk import PlainTextReader
      from hctk.compoAnalysis import CompoAnalysis

      reader = PlainTextReader("data/", auto_load=False)
      c2 = CompoAnalysis(reader)

.. container:: cell markdown

   .. rubric:: 2.1 Frequency Distribution
      :name: 21-frequency-distribution

.. container:: cell code

   .. code:: python

      # Hanzi
      c2.freq_distr(tp="chr", subcorp_idx=0).most_common(10)

   .. container:: output execute_result

      ::

         [('，', 178802),
          ('。', 83819),
          ('之', 64665),
          ('不', 37264),
          ('也', 32634),
          ('而', 32035),
          ('以', 27556),
          ('其', 25931),
          ('者', 23304),
          ('曰', 21763)]

.. container:: cell code

   .. code:: python

      # Shape of hanzi (IDC)
      c2.freq_distr(tp="idc", subcorp_idx=0)

   .. container:: output execute_result

      ::

         Counter({'': 256312,
                  'noChrData': 351898,
                  '⿰': 438079,
                  '⿱': 561453,
                  '⿲': 6242,
                  '⿳': 14381,
                  '⿴': 14409,
                  '⿵': 25234,
                  '⿶': 7275,
                  '⿷': 1641,
                  '⿸': 91226,
                  '⿹': 25384,
                  '⿺': 26847,
                  '⿻': 37847})

.. container:: cell code

   .. code:: python

      # Radical of hanzi
      c2.freq_distr(tp="rad").most_common(10)

   .. container:: output execute_result

      ::

         [('noChrData', 1517367),
          ('人', 422649),
          ('一', 281707),
          ('丿', 252723),
          ('口', 249345),
          ('火', 165875),
          ('言', 157936),
          ('水', 155632),
          ('八', 151539),
          ('心', 145208)]

.. container:: cell code

   .. code:: python

      # Hanzi with a certain radical
      c2.freq_distr(tp=None, radical="广").most_common(10)

   .. container:: output execute_result

      ::

         [('度', 4757),
          ('廣', 4050),
          ('廟', 3067),
          ('府', 3064),
          ('廢', 2542),
          ('庶', 2281),
          ('廉', 1594),
          ('康', 1570),
          ('序', 1213),
          ('庭', 1155)]

.. container:: cell code

   .. code:: python

      # Hanzi with a certain component
      c2.freq_distr(tp=None, compo="水", idc="vert2", pos=-1)

   .. container:: output execute_result

      ::

         Counter({'氶': 1,
                  '汞': 15,
                  '沓': 89,
                  '泉': 1349,
                  '泵': 3,
                  '淼': 4,
                  '滎': 344,
                  '漀': 1,
                  '漐': 9,
                  '漿': 153,
                  '澩': 3,
                  '灓': 5})

.. container:: cell markdown

   .. rubric:: 2.2 Productivity
      :name: 22-productivity

   -  Realized Productivity: :math:`V(C, N)`
   -  Expanding Productivity: :math:`\frac{V(1, C, N)}{V(1, N)}`
   -  Potential Productivity: :math:`\frac{V(1, C, N)}{N(C)}`

.. container:: cell code

   .. code:: python

      # Productivity of a radical
      c2.productivity(radical="广", subcorp_idx=0)

   .. container:: output execute_result

      ::

         {'N': 1858228,
          'NC': 5897,
          'V1': 2083,
          'V1C': 9,
          'productivity': {'expanding': 0.0043206913106096975,
           'potential': 0.001526199762591148,
           'realized': 62}}

.. container:: cell code

   .. code:: python

      # Productivity of a component
      c2.productivity(compo="虫", idc="horz2", pos=0, subcorp_idx=0)

   .. container:: output execute_result

      ::

         {'N': 1858228,
          'NC': 1027,
          'V1': 2083,
          'V1C': 72,
          'productivity': {'expanding': 0.03456553048487758,
           'potential': 0.07010710808179163,
           'realized': 178}}

.. container:: cell code

   .. code:: python

      # Productivity of Hanzi shapes (IDCs)
      import pandas as pd
      from CompoTree import IDC

      df = []
      for idc in IDC:   
          p = c2.productivity(idc=idc.name, subcorp_idx=0)
          df.append({
              'name': idc.name, 
              'shape': idc.value, 
              **p['productivity'],
              'V1C': p['V1C'],
              'V1': p['V1'],
              'NC': p['NC'],
              'N': p['N'],
          })

      df = pd.DataFrame(df)
      df

   .. container:: output execute_result

      ::

              name shape  realized  expanding  potential   V1C    V1      NC        N
         0   horz2     ⿰      5580   0.709073   0.003372  1477  2083  438079  1858228
         1   vert2     ⿱      2110   0.223236   0.000828   465  2083  561453  1858228
         2   horz3     ⿲        37   0.002400   0.000801     5  2083    6242  1858228
         3   vert3     ⿳        85   0.006721   0.000974    14  2083   14381  1858228
         4    encl     ⿴        27   0.001440   0.000208     3  2083   14409  1858228
         5    surN     ⿵        87   0.005761   0.000476    12  2083   25234  1858228
         6    surU     ⿶         6   0.000000   0.000000     0  2083    7275  1858228
         7    curC     ⿷        20   0.001920   0.002438     4  2083    1641  1858228
         8    surT     ⿸       342   0.026884   0.000614    56  2083   91226  1858228
         9    sur7     ⿹        51   0.002880   0.000236     6  2083   25384  1858228
         10   surL     ⿺       180   0.012482   0.000968    26  2083   26847  1858228
         11   over     ⿻        44   0.000960   0.000053     2  2083   37847  1858228

.. container:: cell markdown

   .. rubric:: 3 Ngram Frequency
      :name: 3-ngram-frequency

.. container:: cell code

   .. code:: python

      from hctk import PlainTextReader, Concordancer

      c = Concordancer(PlainTextReader("data/").corpus)

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"139312fcf88f4d288ed2420f4e845446"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"241d4cf67ffd42648fcee02c8d4d6a1e"}

.. container:: cell code

   .. code:: python

      # Bigram frequency
      c.freq_distr_ngrams(n=2, subcorp_idx=0).most_common(10)

   .. container:: output stream stdout

      ::

         Counting 2-grams...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"253235628fd84bc5896ae35eae437e7b"}

   .. container:: output execute_result

      ::

         [('而不', 3913),
          ('天下', 3661),
          ('不可', 2985),
          ('之所', 2723),
          ('子曰', 2581),
          ('人之', 2317),
          ('以為', 2231),
          ('所以', 2023),
          ('不能', 1934),
          ('可以', 1667)]

.. container:: cell code

   .. code:: python

      # Trigram frequency
      c.freq_distr_ngrams(n=3, subcorp_idx=0).most_common(10)

   .. container:: output stream stdout

      ::

         Counting 3-grams...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"5fdaae56638c43fda862f9243ffc3c1a"}

   .. container:: output execute_result

      ::

         [('天下之', 946),
          ('歧伯曰', 766),
          ('之所以', 605),
          ('不可以', 580),
          ('子對曰', 443),
          ('黃帝曰', 403),
          ('此之謂', 350),
          ('子墨子', 343),
          ('孔子曰', 302),
          ('不可不', 298)]

.. container:: cell markdown

   .. rubric:: 4 Collocation
      :name: 4-collocation

.. container:: cell markdown

   .. rubric:: 4.1 Bigram Association
      :name: 41-bigram-association

.. container:: cell code

   .. code:: python

      bi_asso = c.bigram_associations(subcorp_idx=0, sort_by="DeltaP21")
      [x for x in bi_asso if x[1].get('RawCount', 0) > 100][:3]

   .. container:: output execute_result

      ::

         [('歧伯',
           {'DeltaP12': 0.515988379165576,
            'DeltaP21': 0.9870480872578454,
            'Dice': 0.6778754298815437,
            'FisherExact': 0.0,
            'Gsq': 12041.994806908666,
            'MI': 9.41167469710956,
            'RawCount': 887,
            'Xsq': 603675.038957376}),
          ('柰何',
           {'DeltaP12': 0.056661809249506735,
            'DeltaP21': 0.9864357417273106,
            'Dice': 0.10718562874251497,
            'FisherExact': 0.0,
            'Gsq': 2110.3645096843,
            'MI': 8.535527535461881,
            'RawCount': 179,
            'Xsq': 66249.74702510444}),
          ('嗚呼',
           {'DeltaP12': 0.5684168332436602,
            'DeltaP21': 0.9699560936315373,
            'Dice': 0.7168141592920354,
            'FisherExact': 0.0,
            'Gsq': 2772.224707107538,
            'MI': 11.978137468386173,
            'RawCount': 162,
            'Xsq': 653497.5945430023})]

.. container:: cell markdown

   .. rubric:: 4.2 Node-Collocate Association
      :name: 42-node-collocate-association

.. container:: cell code

   .. code:: python

      cql = """
      "孔" "子"
      """
      collo = c.collocates(cql, left=3, right=3, subcorp_idx=0, sort_by="Xsq", alpha=0)
      collo[:5]

   .. container:: output execute_result

      ::

         [('曰',
           {'DeltaP12': 0.5508984202190699,
            'DeltaP21': 0.017436408382199422,
            'Dice': 0.03412938870076635,
            'FisherExact': 0.0,
            'Gsq': 2486.7011528898893,
            'MI': 5.5855958675486095,
            'RawCount': 383,
            'Xsq': 17849.561805227277}),
          ('愀',
           {'DeltaP12': 0.008807342620906026,
            'DeltaP21': 0.4996367483650986,
            'Dice': 0.017316017316017316,
            'FisherExact': 2.1855507492354285e-18,
            'Gsq': 78.36068664097104,
            'MI': 10.41398510902232,
            'RawCount': 6,
            'Xsq': 8177.080337219988}),
          ('孔',
           {'DeltaP12': 0.06707828763041274,
            'DeltaP21': 0.04976704015525816,
            'Dice': 0.05753595997498437,
            'FisherExact': 1.5730409497803884e-81,
            'Gsq': 366.5766447587887,
            'MI': 7.095196721665525,
            'RawCount': 46,
            'Xsq': 6203.299925288661}),
          ('矙',
           {'DeltaP12': 0.002936857562408223,
            'DeltaP21': 0.999634597729232,
            'Dice': 0.005856515373352855,
            'FisherExact': 1.341091030070595e-07,
            'Gsq': 31.652163710326512,
            'MI': 11.41398510902232,
            'RawCount': 2,
            'Xsq': 5455.356826047563}),
          ('問',
           {'DeltaP12': 0.06938851232700384,
            'DeltaP21': 0.022691599983249697,
            'Dice': 0.03471971066907776,
            'FisherExact': 1.0446010447528008e-68,
            'Gsq': 307.47664398618406,
            'MI': 5.973808047464968,
            'RawCount': 48,
            'Xsq': 2925.847560753262})]
