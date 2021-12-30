Stats
================


.. container:: cell markdown

.. container:: cell code

   .. code:: python

      ## Colab setup
      # !gdown https://github.com/liao961120/hgct/raw/main/test/data.zip
      # !unzip -q data.zip
      # !pip install -qU hgct

.. container:: cell markdown

   .. rubric:: Corpus Analysis API in *hgtk*
      :name: corpus-analysis-api-in-hgtk

.. container:: cell markdown

   In this second tutorial, we demonstrate functions for quantitative
   analysis of the corpus in *hgct*. To get started, we need two
   additional objects ``CompoAnalysis`` and ``Dispersion`` in addition
   to the ``Concordancer`` object introduced in the previous tutorial.
   The corpus used is identical to the one in Appendix A.

   Note that when initializing with ``CompoAnalysis()`` and
   ``PlainTextReader()``, the argument ``auto_load=False`` needs to be
   given to ``PlainTextReader()``. This prevents the full corpus to be
   loaded into the memory, such that functionalities provided by
   ``CompoAnalysis`` could be used to analyze large data that do not fit
   into the computer’s memory. For more information, refer to the source
   code on GitHub[1].

   [1]
   https://github.com/liao961120/hgct/blob/main/hgct/compoAnalysis.py

.. container:: cell code

   .. code:: python

      import pandas as pd
      from hgct import PlainTextReader, Concordancer
      from hgct import CompoAnalysis, Dispersion

      CC = Concordancer(PlainTextReader("data/").corpus)
      CA = CompoAnalysis(PlainTextReader("data/", auto_load=False))
      DP = Dispersion(PlainTextReader("data/").corpus)

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"58de1c717dba4b13b447b9c9d19e02b7"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"638bc9b3e1e740fcb0332d33fd692876"}

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"23eb85e2194a4cbb82db8031596b9b29"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"dbe1ae734bfa43baac59822da8c1059b"}

.. container:: cell markdown

   .. rubric:: Frequency List (Distribution)
      :name: frequency-list-distribution

   Frequency lists are provided by the function
   ``CompoAnalysis.freq_distr()``. Based on the arguments passed, this
   function computes and returns the frequency distribution of either
   the characters, IDCs, Kangxi radicals, or characters with a given
   radical/component. Below, we demonstrate each of these types of
   frequency distributions.

.. container:: cell markdown

   .. rubric:: Character
      :name: character

   To return the frequency distribution of the characters in the corpus,
   set the argument ``tp`` to ``"chr"``. ``CompoAnalysis.freq_distr()``
   by default returns a ``Counter``\ [1], which has the convenient
   method ``most_common()`` that could be used to retrieve the terms
   with the highest frequencies.

   [1]
   https://docs.python.org/3/library/collections.html#collections.Counter

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp="chr").most_common(4)

   .. container:: output execute_result

      ::

         [('之', 210608), ('不', 129212), ('也', 107639), ('以', 104578)]

.. container:: cell markdown

   As mentioned in @sec:app-search-by-character, we could limit the
   scope of calculation to a particular subcorpus by specifying its
   index. To do this, pass the argument ``subcorp_idx`` to the function.
   The example below sets the subcorpus to ``3``, which is the subcorpus
   of modern Chinese (ASBC).

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp="chr", subcorp_idx=3).most_common(4)

   .. container:: output execute_result

      ::

         [('的', 15826), ('一', 5537), ('是', 5130), ('不', 4469)]

.. container:: cell markdown

   .. rubric:: IDC
      :name: idc

   Frequency distributions of the Ideographic Description Characters
   (IDCs) could similarly be retrieved by setting ``tp`` to ``"idc"``.
   Note that there is an argument ``use_chr_types`` that applies when
   ``tp="idc"`` (IDC) or ``tp="rad"`` (radical). ``use_chr_types`` is
   used to determine how to compute the frequencies. If it is set to
   ``False``, character frequencies are considered. If it is ``True``,
   character frequencies are discarded. In other words, when
   ``use_chr_types=False``, an IDC or a radical would only be counted
   once for each type of character. See @sec:frequency-lists for a toy
   example.

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp="idc", subcorp_idx=3)

   .. container:: output execute_result

      ::

         Counter({'': 48725,
                  '⿰': 167681,
                  '⿱': 120035,
                  '⿲': 1965,
                  '⿳': 4068,
                  '⿴': 5744,
                  '⿵': 7834,
                  '⿶': 1637,
                  '⿷': 537,
                  '⿸': 18511,
                  '⿹': 4412,
                  '⿺': 13451,
                  '⿻': 10324})

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp="idc", use_chr_types=True, subcorp_idx=3)

   .. container:: output execute_result

      ::

         Counter({'': 119,
                  '⿰': 2454,
                  '⿱': 1019,
                  '⿲': 26,
                  '⿳': 39,
                  '⿴': 18,
                  '⿵': 45,
                  '⿶': 6,
                  '⿷': 12,
                  '⿸': 176,
                  '⿹': 41,
                  '⿺': 123,
                  '⿻': 32})

.. container:: cell markdown

   .. rubric:: Radical
      :name: radical

   To retrieve frequency distributions for radicals, set ``tp="rad"``.
   The usage of ``use_chr_types`` here is similar to the IDC described
   above.

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp="rad", subcorp_idx=3).most_common(4)

   .. container:: output execute_result

      ::

         [('人', 28149), ('白', 16640), ('一', 15567), ('口', 15443)]

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp="rad", use_chr_types=True, subcorp_idx=3).most_common(4)

   .. container:: output execute_result

      ::

         [('水', 233), ('口', 207), ('手', 201), ('人', 172)]

.. container:: cell markdown

   .. rubric:: Characters with a given radical
      :name: characters-with-a-given-radical

   It is also possible to look into characters of a specific type. By
   setting ``tp=None``, one could then pass in a radical to the argument
   ``radical`` to look at the frequency distribution of the characters
   with this particular radical.

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp=None, radical="广").most_common(4)

   .. container:: output execute_result

      ::

         [('度', 4757), ('廣', 4050), ('廟', 3067), ('府', 3064)]

.. container:: cell markdown

   .. rubric:: Characters with a given IDC component
      :name: characters-with-a-given-idc-component

   Similarly, a frequency distribution of characters of a specific type
   defined according to a component and an optional IDC describing the
   the shape could also be retrieved by specifying ``tp=None`` and the
   arguments ``compo`` and ``idc`` (optional).

.. container:: cell code

   .. code:: python

      CA.freq_distr(tp=None, compo="水", idc="vert2")

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

   .. rubric:: Dispersion
      :name: dispersion

   Measures of dispersion could be calculated based on a character or a
   search pattern.

.. container:: cell markdown

   .. rubric:: Dispersion Measures for Characters
      :name: dispersion-measures-for-characters

   ``Dispersion.char_dispersion()`` is used for calculating dispersion
   measures for a character. The examples below—using the toy corpus in
   Gries (2020)—demonstrate the validity of the returned measure. The
   values should be identical to those in Table 1 of Gries (2020).

.. container:: cell code

   .. code:: python

      # Gries (2020, Table 1)
      DP.char_dispersion(char='a', subcorp_idx=4)

   .. container:: output execute_result

      ::

         {'DP': 0.18,
          'DPnorm': 0.2195121951219512,
          'JuillandD': 0.7851504534504508,
          'KLdivergence': 0.13697172936522078,
          'Range': 5,
          'RosengrenS': 0.9498163423042408}

.. container:: cell code

   .. code:: python

      # return_raw=True to get the raw data for dispersion calculation
      DP.char_dispersion(char='a', return_raw=True, subcorp_idx=4)

   .. container:: output execute_result

      ::

         ({'DP': 0.18,
           'DPnorm': 0.2195121951219512,
           'JuillandD': 0.7851504534504508,
           'KLdivergence': 0.13697172936522078,
           'Range': 5,
           'RosengrenS': 0.9498163423042408},
          {'corpus_size': 50,
           'f': 15,
           'n': 5,
           'p': [0.1111111111111111, 0.45454545454545453, 0.3, 0.2, 0.4],
           's': [0.18, 0.22, 0.2, 0.2, 0.2],
           'v': [1, 5, 3, 2, 4]})

.. container:: cell markdown

   To see how dispersion measures behave on real data, we calculate
   dispersion measures for four characters (之, 也, 草, and 巾) in a
   corpus of Literary Chinese texts. The first two characters 之 and 也
   are often used as function words and the last two as content words in
   Literary Chinese. Hence, we would expect the first two to be
   distributed evenly, and the latter two unevenly in the corpus.

.. container:: cell code

   .. code:: python

      subcorp_idx = 0
      df_disp = []
      for ch in '之也草巾':
          stats, raw = DP.char_dispersion(
              char=ch, subcorp_idx=subcorp_idx, return_raw=True
          )
          d = {
              'char': ch,
              'Range(%)': '{:.2f}'.format(100 * stats['Range'] / raw['n']),
              **stats
          }
          df_disp.append(d)
      df_disp = pd.DataFrame(df_disp)
      df_disp

   .. container:: output execute_result

      ::

           char Range(%)  Range        DP    DPnorm  KLdivergence  JuillandD  RosengrenS
         0    之    90.98    666  0.128508  0.128509      0.095890   0.977316    0.961405
         1    也    77.05    564  0.251459  0.251462      0.401038   0.962913    0.823893
         2    草    22.40    164  0.649643  0.649649      2.331477   0.863829    0.320790
         3    巾     3.69     27  0.844676  0.844683      4.077689   0.541787    0.101871

.. container:: cell markdown

   .. rubric:: Dispersion Measures of Complex Forms (defined by CQL)
      :name: dispersion-measures-of-complex-forms-defined-by-cql

   Dispersion measures for abstract units could also be calculated with
   the returned concordance lines provided by
   ``Concordancer.cql_search()``. The function
   ``DP.pattern_dispersion()`` is designed to take the queried results
   from ``Concordancer.cql_search()`` to calculate dispersion measures.

.. container:: cell code

   .. code:: python

      cql = """
      [semtag="人體精神"] [semtag="人體精神"]
      """
      results = list(CC.cql_search(cql, left=3, right=3))
      print('Num of results:', len(results))
      for r in results[:3]: print(r)

   .. container:: output stream stdout

      ::

         Num of results: 8459
         <Concord 。有孚{惠心}，勿問>
         <Concord 大澤則{惠必}及下，>
         <Concord 「仁義{惠愛}而已矣>

.. container:: cell code

   .. code:: python

      DP.pattern_dispersion(data=results, subcorp_idx=2)

   .. container:: output execute_result

      ::

         {'DP': 0.1504848557289626,
          'DPnorm': 0.15050344195568013,
          'JuillandD': 0.9387038720245429,
          'KLdivergence': 0.135483902941753,
          'Range': 134,
          'RosengrenS': 0.9428568965311757}

.. container:: cell markdown

   The example below calculates dispersion measures for **each subcorpus
   0, 1, and 2**. This is useful when the user is interested in
   contrasting dispersion measures in different corpora (e.g.,
   genre/diachronic comparison).

.. container:: cell code

   .. code:: python

      # Compute separate dispersion measures for each subcorpus
      df_pat_disp = []
      for i in range(3):
          stats, raw = DP.pattern_dispersion(
              data=results, subcorp_idx=i, return_raw=True
          )
          d = {
              'Range(%)': '{:.2f}'.format(100 * stats['Range'] / raw['n']),
              **stats,
              'freq': raw['f'],
              'corp_size': raw['corpus_size']
          }
          df_pat_disp.append(d)
      df_pat_disp = pd.DataFrame(df_pat_disp)
      df_pat_disp

   .. container:: output execute_result

      ::

           Range(%)  Range        DP    DPnorm  ...  JuillandD  RosengrenS  freq  corp_size
         0    44.40    325  0.399226  0.399229  ...   0.907705    0.629630  1689    1858228
         1    53.38    560  0.325007  0.325008  ...   0.950161    0.753668  3500    3938310
         2    85.90    134  0.150485  0.150503  ...   0.938704    0.942857  2489    2097273

         [3 rows x 9 columns]

.. container:: cell markdown

   .. rubric:: Ngram Frequency
      :name: ngram-frequency

   We now turn to the relationships across characters. To compute
   character n-grams, one can use ``Concordancer.freq_distr_ngrams()``.

.. container:: cell code

   .. code:: python

      CC.freq_distr_ngrams(n=2, subcorp_idx=0).most_common(4)

   .. container:: output stream stdout

      ::

         Counting 2-grams...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"bb5037e60ea8460abcc2e2050bd94200"}

   .. container:: output execute_result

      ::

         [('而不', 3913), ('天下', 3661), ('不可', 2985), ('之所', 2723)]

.. container:: cell code

   .. code:: python

      CC.freq_distr_ngrams(n=3, subcorp_idx=0).most_common(4)

   .. container:: output stream stdout

      ::

         Counting 3-grams...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"98917c323e1943c694386d79c257604f"}

   .. container:: output execute_result

      ::

         [('天下之', 946), ('歧伯曰', 766), ('之所以', 605), ('不可以', 580)]

.. container:: cell markdown

   .. rubric:: Collocation
      :name: collocation

   Association measures could be used to quantify the strengths of
   attraction between a pair of characters. Pairs with strong
   attractions could be considered as collocations. *hgct* implements
   two types of collocation extraction functions. The first
   (``Concordancer.bigram_associations()``) is based on bigrams, which
   simply computes association scores for all bigrams. With the second
   implementation (``Concordancer.collocates()``), users could specify a
   node and a window size, and characters falling within this window
   around the node would be treated as a node-collocate pair. Each pair
   is then computed for an association score.

.. container:: cell markdown

   .. rubric:: Bigram Association
      :name: bigram-association

.. container:: cell code

   .. code:: python

      bi_asso = CC.bigram_associations(subcorp_idx=3, sort_by="Gsq")
      bi_asso[0]

   .. container:: output execute_result

      ::

         ('自己',
          {'DeltaP12': 0.9778668701918644,
           'DeltaP21': 0.36342714003090937,
           'Dice': 0.5303392259913999,
           'FisherExact': 0.0,
           'Gsq': 6188.677676112116,
           'MI': 7.855905225817536,
           'RawCount': 555,
           'Xsq': 128210.23324106314})

.. container:: cell code

   .. code:: python

      d = pd.DataFrame([{'bigram': x[0], **x[1]} for x in bi_asso][:5])
      # print(d.to_markdown(index=False, floatfmt=".2f", numalign="left"))
      d

   .. container:: output execute_result

      ::

           bigram        MI            Xsq  ...  DeltaP12  FisherExact  RawCount
         0     自己  7.855905  128210.233241  ...  0.977867          0.0       555
         1     什麼  9.153258  192859.824384  ...  0.547635          0.0       339
         2     我們  6.183966   42280.224680  ...  0.446638          0.0       592
         3     台灣  8.126771  111740.169937  ...  0.693597          0.0       401
         4     沒有  6.394685   43012.134830  ...  0.164128          0.0       518

         [5 rows x 9 columns]

.. container:: cell markdown

   .. rubric:: Node-Collocate Association
      :name: node-collocate-association

   The example below use the character sequence ``我們`` as the node and
   looks for collocates occurring on the immediate right (``left=0`` and
   ``right=1``) on the node. After computing association scores for each
   node-collocate pair, these pairs are sorted based on the MI measure.
   The data frame below shows the top-5 collocates with the highest MI
   scores (a minimum frequency threshold of 6 is applied) of the node
   ``我們``.

.. container:: cell code

   .. code:: python

      cql = """
      [char="我"] [char="們"]
      """
      collo = CC.collocates(cql, left=0, right=1, subcorp_idx=3, 
                            sort_by="MI", alpha=0)
      collo[0]

   .. container:: output execute_result

      ::

         ('釘',
          {'DeltaP12': 0.0016848237685590844,
           'DeltaP21': 0.33204500782950214,
           'Dice': 0.0033613445378151263,
           'FisherExact': 0.003866505328061448,
           'Gsq': 9.493215334772461,
           'MI': 8.012895027477056,
           'RawCount': 1,
           'Xsq': 256.6351579547297})

.. container:: cell code

   .. code:: python

      d = pd.DataFrame([{'char': x[0], **x[1]} for x in collo 
                        if x[1]['RawCount'] > 5][:5])
      #print(d.to_markdown(index=False, floatfmt=".2f", numalign="left"))
      d

   .. container:: output execute_result

      ::

           char        MI         Xsq  ...  DeltaP12   FisherExact  RawCount
         0    認  3.979880  124.857368  ...  0.014258  9.310853e-09         9
         1    還  3.388404   77.315368  ...  0.013769  2.970053e-07         9
         2    都  3.328575  122.653021  ...  0.022845  6.215205e-11        15
         3    就  3.207562  125.435532  ...  0.025641  1.218295e-11        17
         4    所  3.047111   76.926085  ...  0.017841  4.222232e-08        12

         [5 rows x 9 columns]

.. container:: cell markdown

   .. rubric:: Productivity
      :name: productivity

   Finally, we demonstrate the usage of the tentative applications of
   Productivity measures [@\ baayen1993;@baayen2009] to character
   components. This is implemented in ``CompoAnalysis.productivity()``.
   The categories for computing measures of productivity are defined
   based on the arguments passed.

.. container:: cell code

   .. code:: python

      # Productivity of a radical
      CA.productivity(radical="广", subcorp_idx=0)

   .. container:: output execute_result

      ::

         {'N': 1505967,
          'NC': 5889,
          'V1': 1896,
          'V1C': 7,
          'productivity': {'expanding': 0.003691983122362869,
           'potential': 0.0011886568177958906,
           'realized': 58}}

.. container:: cell code

   .. code:: python

      # Productivity of a component
      CA.productivity(compo="虫", idc="horz2", pos=0, subcorp_idx=0)

   .. container:: output execute_result

      ::

         {'N': 1505967,
          'NC': 1027,
          'V1': 1896,
          'V1C': 72,
          'productivity': {'expanding': 0.0379746835443038,
           'potential': 0.07010710808179163,
           'realized': 178}}

.. container:: cell code

   .. code:: python

      # Productivity of Hanzi shapes (IDCs)
      df_prod = []
      for idc_nm, idc_val in CC.chr_idcs.items():   
          p = CA.productivity(idc=idc_nm, subcorp_idx=0)
          df_prod.append({
              'name': idc_nm, 
              'shape': idc_val, 
              **p['productivity'],
              'V1C': p['V1C'],
              'V1': p['V1'],
              'NC': p['NC'],
              'N': p['N'],
          })

      df_prod = pd.DataFrame(df_prod)
      df_prod

   .. container:: output execute_result

      ::

              name shape  realized  expanding  potential   V1C    V1      NC        N
         0   horz2     ⿰      5436   0.719409   0.003115  1364  1896  437854  1505967
         1   vert2     ⿱      2045   0.219409   0.000741   416  1896  561357  1505967
         2   horz3     ⿲        35   0.001582   0.000481     3  1896    6240  1505967
         3   vert3     ⿳        80   0.005802   0.000765    11  1896   14371  1505967
         4    encl     ⿴        27   0.001582   0.000208     3  1896   14409  1505967
         5    surN     ⿵        84   0.004747   0.000357     9  1896   25231  1505967
         6    surU     ⿶         6   0.000000   0.000000     0  1896    7275  1505967
         7    curC     ⿷        20   0.002110   0.002438     4  1896    1641  1505967
         8    surT     ⿸       332   0.026371   0.000548    50  1896   91208  1505967
         9    sur7     ⿹        48   0.002637   0.000197     5  1896   25379  1505967
         10   surL     ⿺       178   0.013186   0.000931    25  1896   26844  1505967
         11   over     ⿻        43   0.000527   0.000026     1  1896   37846  1505967
