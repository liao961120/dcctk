Query
================


.. container:: cell markdown

.. container:: cell code

   .. code:: python

      # # Colab setup
      # !gdown https://github.com/liao961120/hgct/raw/main/test/data.zip
      # !unzip -q data.zip
      # !pip install -qU hgct

.. container:: cell markdown

   .. raw:: html

      <!-- Hide section entries in toc -->

   .. rubric:: Search API in *hgtk*
      :name: search-api-in-hgtk

.. container:: cell markdown

   In the following tutorials (Appendix A and B), we will use a small
   collection of texts as the example corpus. The text data is available
   on GitHub at
   https://github.com/liao961120/hgct/raw/main/test/data.zip. After
   extracting ``data.zip`` to the directory ``data``, it should have the
   following structure:

   ::

      data
      ├── 01
      │   ├── 儀禮_公食大夫禮.txt
      │   ├── ...
      │   └── 黃帝內經_靈樞經.txt
      ├── 02
      │   ├── ...
      │   └── 鹽鐵論_卷四.txt
      ├── 03
      │   ├── 三國志_吳書一.txt
      │   ├── ...
      │   └── 魯勝墨辯注敘_魯勝墨辯注敘.txt
      ├── 08
      │   ├── asbc1.txt
      │   └── asbc2.txt
      └── 10
          ├── dispersion1.txt
          ├── ...
          └── dispersion5.txt

   The directory ``data`` corresponds to the corpus in *hgct*\ ’s corpus
   representation. It contains five directories, each of which
   corresponds to a subcorpus. Directory ``01``, ``02``, and ``03``
   consists of small samples of Literary Chinese texts collected from
   the Chinese Text Project (https://ctext.org). Directory ``08`` holds
   modern Chinese texts sampled from ASBC. The directory ``10`` is a toy
   corpus in @gries2020 [p. 102] used for illustrating calculations of
   dispersion measures.

.. container:: cell markdown

   In this tutorial, we demonstrate the supported functionalities in
   *hgct* for searching the corpus.

   .. rubric:: Loading Corpus Data into Concordancer
      :name: loading-corpus-data-into-concordancer

   Provided that the input corpus follows the required directory
   structure mentioned in @sec:corpus-structure-and-input-data, users
   could convert the input corpus to the internal corpus representation
   with ``PlainTextReader()`` as in the following code block. Since we
   are now demonstrating the search functions, we immediately pass the
   corpus to ``Concordancer()``, which is the object used in *hgct* for
   searching the corpus.

.. container:: cell code

   .. code:: python

      from hgct import PlainTextReader, Concordancer
      c = Concordancer(PlainTextReader("data/").corpus)

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"fb6872ef86e3446da7140a66c9108fc0"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"3502b87c9fab4b1aabfd8a07bcf460dc"}

.. container:: cell markdown

   The ``Concordancer`` object could be used to retrieve results
   matching the search pattern as a sequence[1] of concordance lines.
   Since many of the search patterns would return plenty of results, we
   define a wrapper function ``get_first_n()`` here for the purpose of
   demonstration.

   [1] More precisely, a *generator* of concordance lines.

.. container:: cell code

   .. code:: python

      def get_first_n(cql, n=10, left=5, right=5):
          out = []
          for i, r in enumerate(c.cql_search(cql, left=left, right=right)):
              if i == n: break
              out.append(r)
          return out

.. container:: cell markdown

   .. rubric:: Search by Character
      :name: search-by-character

   In our first example, we define the search pattern as
   ``[char="龜"] [char="[一-龜]"]``, which roughly means

      a sequence of two characters starting with “龜” and ending with
      any Chinese characters (not, e.g., punctuations)

   Passing this pattern to ``get_first_n()`` (or
   ``Concordancer.cql_search()``) gives us a sequence of ``Concord``
   objects. A ``Concord`` object is used to represent a matched result
   returned from the corpus in *hgct*.

.. container:: cell code

   .. code:: python

      cql = '''
      [char="龜"] [char="[一-龜]"]
      '''
      # left/right: left/right context size around the keyword
      results = get_first_n(cql, n=5, left=6, right=3)  
      results

   .. container:: output execute_result

      ::

         [<Concord 遷有無，貨自{龜貝}，至此>,
          <Concord 山在西北。有{龜山}。有龍>,
          <Concord ，故獸不狘；{龜以}為畜，>,
          <Concord 江郡常歲時生{龜長}尺二寸>,
          <Concord 無為頓復卜三{龜知}。聖人>]

.. container:: cell markdown

   To get more information about a particular matching result, we can
   look at the ``data`` attribute in a ``Concord`` object, which is a
   dictionary holding the relevant information of the matching result.

.. container:: cell code

   .. code:: python

      result_1 = results[0]
      result_1.data

   .. container:: output execute_result

      ::

         {'captureGroups': {},
          'keyword': '龜貝',
          'left': '遷有無，貨自',
          'meta': {'id': '02/漢書_傳.txt',
           'text': {'book': '漢書', 'sec': '傳'},
           'time': {'label': '漢', 'ord': 2, 'time_range': [-205, 220]}},
          'position': (1, 6, 3482, 42),
          'right': '，至此'}

.. container:: cell markdown

   Note the ``position`` key in ``Concord.data``. It holds the position
   of the matched keyword in the corpus. The elements in the 4-tuple
   ``(1, 6, 3482, 32)`` correspond respectively to the indices of
   ``(subcorpus, text, sentence, character)``.

   We did not mention above how the index of a subcorpus is determined.
   The index of a subcorpus is automatically determined according to the
   **character order of the directory names**. Remember that there are
   four directories (subcorpora) in our input corpus---``01``, ``02``,
   ``03``, ``08``, and ``10``. So by character order, ``01`` appears
   before ``02``, ``02`` before ``03``, ``03`` before ``08``, and so on.
   Hence, the first directory ``01`` is given the index of 0, the second
   is given the index of 1, and so on. These indices of the subcorpora,
   as seen later in Appendix B, could be used for limiting the scope of
   the functions in *hgct* in computing corpus statistical measures.

.. container:: cell markdown

   .. rubric:: Search by Character Components
      :name: search-by-character-components

   In addition to character forms, we can also describe search patterns
   in terms of character compositions, such as the Kangxi Radical or
   Ideographic Descriptions of a character.

.. container:: cell markdown

   .. rubric:: Kangxi Radicals
      :name: kangxi-radicals

   To take a look at all the present Kangxi radicals in the characters
   of the corpus, the attribute ``Concordancer.chr_radicals`` could be
   used:

.. container:: cell code

   .. code:: python

      print(c.chr_radicals)

   .. container:: output stream stdout

      ::

         Building index for character radicals...
         {'', '钅', '鬲', '高', '見', '广', '片', '黹', '自', '尸', '鬥', '屮', '面', '麦', '攴', '糸', '臣', '丨', '車', '鱼', '毛', '饣', '癶', '舟', '鼓', '襾', '鹿', '龜', '欠', '香', '鼻', '干', '臼', '爪', '缶', '隶', '用', '走', '爻', '风', '食', '貝', '夕', '刀', '丿', '黍', '匸', '女', '疒', '火', '目', '穴', '卜', '白', '宀', '耒', '曰', '冖', '廾', '力', '支', '老', '匚', '方', '長', '冂', '黽', '冫', '巾', '而', '虫', '尢', '齒', '耳', '入', '手', '鸟', '鳥', '厶', '瓦', '勹', '彐', '车', '凵', '气', '辵', '田', '牙', '龙', '羽', '十', '网', '匕', '辰', '氏', '皮', '角', '豆', '齿', '衣', '首', '矛', '革', '犬', '米', '禾', '生', '豸', '页', '非', '羊', '贝', '玄', '毋', '卩', '歹', '隹', '色', '见', '龟', '禸', '鼎', '鼠', '木', '弓', '至', '皿', '谷', '馬', '韦', '魚', '辛', '彳', '二', '血', '廴', '瓜', '殳', '夂', '言', '厂', '讠', '肉', '靑', '虍', '音', '牛', '豕', '髟', '囗', '石', '龠', '斤', '黑', '玉', '甘', '水', '竹', '雨', '小', '止', '黃', '示', '亠', '麥', '士', '邑', '齊', '土', '鬯', '釆', '戈', '足', '心', '月', '口', '乙', '舛', '亅', '頁', '龍', '酉', '工', '阜', '立', '弋', '日', '黾', '矢', '纟', '寸', '无', '人', '彡', '丶', '己', '麻', '聿', '鹵', '儿', '艮', '几', '艸', '骨', '门', '韋', '巛', '韭', '山', '文', '風', '門', '行', '疋', '马', '身', '又', '斗', '戶', '幺', '赤', '金', '舌', '子', '爿', '鬼', '一', '里', '大', '飛', '夊', '比', '父', '八'}

.. container:: cell markdown

   To search the corpus with Kangxi radicals, simply use the attribute
   ``radical`` in the description of the search pattern.

.. container:: cell code

   .. code:: python

      cql = '''
      [radical="立"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 屬皆从立。{䇐}：臨也。从>,
          <Concord 从立卑聲。{竲}：北地高樓>,
          <Concord 也。从口歫{䇂}。䇂，惡聲>,
          <Concord 从口歫䇂。{䇂}，惡聲也。>,
          <Concord 曰語。从口{䇂}聲。凡言之>]

.. container:: cell markdown

   .. rubric:: Ideographic Description Characters (IDCs)
      :name: ideographic-description-characters-idcs

   Character components defined according to the Unicode’s Ideographic
   Description Characters (IDCs) could also be used for searching. The
   IDCs and their names in *hgct* are found in
   ``Concordancer.chr_idcs``:

.. container:: cell code

   .. code:: python

      c.chr_idcs

   .. container:: output execute_result

      ::

         {'curC': '⿷',
          'encl': '⿴',
          'horz2': '⿰',
          'horz3': '⿲',
          'over': '⿻',
          'sur7': '⿹',
          'surL': '⿺',
          'surN': '⿵',
          'surT': '⿸',
          'surU': '⿶',
          'vert2': '⿱',
          'vert3': '⿳'}

.. container:: cell markdown

   To search according to Ideographic Descriptions, use the attributes
   ``compo`` and/or ``idc``.

.. container:: cell code

   .. code:: python

      cql = '''
      [compo="木" & idc="vert2" & pos="0"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 城。趙國豪{杰}之士，多在>,
          <Concord ，百人者曰{杰}，十人者曰>,
          <Concord 者曰豪。豪{杰}俊英不相陵>,
          <Concord ：并當時之{杰}筆也。觀伯>,
          <Concord 并辭賦之英{杰}也。及仲宣>]

.. container:: cell code

   .. code:: python

      cql = '''
      [compo="木" & idc="vert2" & pos="1"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 有甬，官食{槩}，不可以辟>,
          <Concord 从木午聲。{槩}：𣏙斗斛。>,
          <Concord 郢，而封夫{槩}於堂谿，為>,
          <Concord 幾夷、皓之{槩}。周羣占天>,
          <Concord 質直，皆節{槩}梗梗，有大>]

.. container:: cell code

   .. code:: python

      cql = '''
      [compo="木" & idc="vert2"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 子國為客，{樂}及遍舞。鄭>,
          <Concord 舉，而況敢{樂}禍乎！今吾>,
          <Concord 歌舞不息，{樂}禍也。夫出>,
          <Concord 忘憂，是謂{樂}禍，禍必及>,
          <Concord ，君欣欣兮{樂}康。浴蘭湯>]

.. container:: cell markdown

   Either ``compo`` or ``idc`` could be left out if a more abstract
   search pattern is preferred. For instance, if the shape (``idc``) and
   the position (``pos``) are not of interest, these attributes could be
   left out.

.. container:: cell code

   .. code:: python

      cql = '''
      [compo="木"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 藟，施于條{枚}；凱弟君子>,
          <Concord 四綍，皆銜{枚}，司馬執鐸>,
          <Concord 後。兩軍𠾑{枚}，或左或右>,
          <Concord 徒二人。銜{枚}氏：下士二>,
          <Concord 矢射之。銜{枚}氏：掌司囂>]

.. container:: cell markdown

   If one is interested only in the shape of the character, ``idc``
   could be specified while all other attributes could be left out.

.. container:: cell code

   .. code:: python

      cql = '''
      [idc="encl"] [idc="encl"]
      '''
      get_first_n(cql, 5)

   .. container:: output stream stdout

      ::

         Building index for character IDCs...

   .. container:: output execute_result

      ::

         [<Concord ：『始舍之{圉圉}焉，少則洋>,
          <Concord 公朝虜而子{圉夕}立，更始尚>,
          <Concord 𢦔聲。軍：{圜圍}也。四千人>,
          <Concord 永昌」，方{圜四}寸，上紐交>,
          <Concord 行天下，雖{困四}夷，人莫不>]

.. container:: cell markdown

   .. rubric:: Radical Semantic Type
      :name: radical-semantic-type

   Ma’s (2016) semantic type classification of Kangxi Radicals is also
   incorporated in *hgct*\ ’s search function. Use the attribute
   ``semtag`` to specify a radical semantic type. Refer to
   @tbl:ma2016-radical for the 22 available semantic types.

.. container:: cell code

   .. code:: python

      cql = '''
      [semtag="植物"] [semtag="植物"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 兮水中，搴{芙蓉}兮木末。心>,
          <Concord 兮陳坐，援{芙蕖}兮為蓋。水>,
          <Concord 宿兮石城。{芙蓉}蓋而蔆華車>,
          <Concord 而緣木。因{芙蓉}而為媒兮，>,
          <Concord 為衣兮，集{芙蓉}以為裳。不>]

.. container:: cell markdown

   .. rubric:: Search by Phonetic Properties
      :name: search-by-phonetic-properties

   *hgct* also provides searching the corpus with sound properties. The
   sound properties are defined according to the data from two
   system—Guanyun 廣韻 (Middle Chinese) and Chinese Dictionary compiled
   by the Ministry of Education (MOE) in Taiwan (Mandarin).

.. container:: cell code

   .. code:: python

      c.cql_attrs['CharPhonetic']

   .. container:: output execute_result

      ::

         {'moe': ['phon', 'tone', 'tp', 'sys="moe"'],
          '廣韻': ['攝', '聲調', '韻母', '聲母', '開合', '等第', '反切', '拼音', 'IPA', 'sys="廣韻"']}

.. container:: cell markdown

   .. rubric:: Mandarin (based on 萌典)
      :name: mandarin-based-on-萌典

.. container:: cell code

   .. code:: python

      cql = '''
      [phon="ㄨㄥ" & tone="1" & sys="moe"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 」耳邊不斷{嗡}嗡的縈繞著>,
          <Concord 耳邊不斷嗡{嗡}的縈繞著類>,
          <Concord 市朝也。而{翁}不爭焉，顧>,
          <Concord 發猛，塤篪{翁}博，瑟易良>,
          <Concord ，黑文而赤{翁}，名曰櫟，>]

.. container:: cell code

   .. code:: python

      cql = '''
      [phon="^p" & tp="ipa" & sys="moe"] [phon="^p" & tp="ipa" & sys="moe"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 荒亂，以十{破百}。器備不行>,
          <Concord 戰而赴圍。{破伯}牙之號鍾兮>,
          <Concord 應弱燕，燕{破必}矣。燕破則>,
          <Concord 分離，陰陽{破敗}，經絡厥絕>,
          <Concord 而弓秦，秦{破必}矣。今見破>]

.. container:: cell markdown

   .. rubric:: Middle Chinese (based on 廣韻)
      :name: middle-chinese-based-on-廣韻

.. container:: cell code

   .. code:: python

      cql = '''
      [韻母="東" & 聲調="平" & sys="廣韻"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 曾參之參。{梵}：出自西域>,
          <Concord 薨奏焉。樊{梵}，字文高，>,
          <Concord 曆編訢、李{梵}等綜校其狀>,
          <Concord 行。而訢、{梵}猶以為元首>,
          <Concord 蘇統及訢、{梵}等十人。以>]
