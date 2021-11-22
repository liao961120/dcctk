Query
================


.. container:: cell markdown

.. container:: cell code

   .. code:: python

      !gdown https://github.com/liao961120/hctk/raw/main/test/data.zip
      !unzip -q data.zip
      !pip install -q https://github.com/liao961120/CompoTree/tarball/main
      !pip install -qU hctk

   .. container:: output stream stdout

      ::

         Downloading...
         From: https://github.com/liao961120/hctk/raw/main/test/data.zip
         To: /content/data.zip
         100% 11.5M/11.5M [00:00<00:00, 99.7MB/s]
         poTree (setup.py) ... ents to build wheel ... etadata ... 

.. container:: cell code

   .. code:: python

      from hctk import PlainTextReader
      from hctk import Concordancer

      c = Concordancer(PlainTextReader("data/").corpus)

   .. container:: output stream stdout

      ::

         Indexing corpus for text retrival...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"88734e113f194da29701f2d8f90a1dfa"}

   .. container:: output stream stdout

      ::

         Indexing corpus for concordance search...

   .. container:: output display_data

      .. code:: json

         {"version_major":2,"version_minor":0,"model_id":"1115561dfd004ccd85328a09458d1a42"}

.. container:: cell code

   .. code:: python

      def get_first_n(cql, n=10):
          out = []
          for i, result in enumerate(c.cql_search(cql)):
              if i == n: break
              out.append(result)
          return out

.. container:: cell markdown

   .. rubric:: 1 Search by Character
      :name: 1-search-by-character

.. container:: cell code

   .. code:: python

      cql = '''
      [char="龜"] [char="[一-龜]"]
      '''
      get_first_n(cql, 10)

   .. container:: output execute_result

      ::

         [<Concord 曰：「十戰{龜熸}，是荊人也>,
          <Concord 坤之卦，蓍{龜者}則卜筮之數>,
          <Concord ，毛蚡蜦；{龜知}，背負文。>,
          <Concord 尚生不死。{龜能}行氣導引。>,
          <Concord 為兒時，以{龜枝}床，至後老>,
          <Concord 死，移床，{龜尚}生不死。龜>,
          <Concord 為寶貨。元{龜為}蔡，非四民>,
          <Concord 也。脩肱而{龜背}，長九尺有>,
          <Concord 妖。時則有{龜孽}。時則有雞>,
          <Concord 起離體泉，{龜蛟}珠蛤。土為>]

.. container:: cell markdown

   .. rubric:: 2 Search by Character Component
      :name: 2-search-by-character-component

   .. rubric:: 2.1 Radicals of all characters found in the corpus
      :name: 21-radicals-of-all-characters-found-in-the-corpus

.. container:: cell code

   .. code:: python

      print(c.chr_radicals)

   .. container:: output stream stdout

      ::

         Building index for character radicals...
         {'', '風', '長', '齿', '鬥', '米', '鳥', '皮', '干', '阜', '木', '鬼', '韋', '釆', '亅', '玄', '辰', '宀', '刀', '支', '韭', '舟', '田', '饣', '止', '癶', '辵', '鱼', '夕', '馬', '弓', '示', '欠', '疋', '车', '龙', '方', '缶', '己', '爿', '隹', '鸟', '非', '士', '纟', '卜', '鼎', '乙', '革', '見', '豸', '走', '羊', '匕', '马', '麥', '寸', '麦', '身', '黑', '殳', '犬', '隶', '女', '黾', '甘', '亠', '页', '酉', '火', '心', '龍', '水', '韦', '卩', '氏', '虫', '豕', '人', '瓜', '爻', '牛', '口', '小', '毋', '儿', '目', '矛', '而', '玉', '鬯', '香', '廾', '雨', '龠', '手', '囗', '黍', '气', '角', '广', '文', '山', '戈', '邑', '门', '赤', '髟', '鼠', '几', '廴', '門', '里', '白', '鼻', '生', '麻', '见', '丶', '老', '臣', '土', '肉', '钅', '无', '襾', '艸', '日', '齒', '大', '爪', '鹿', '丿', '攴', '冂', '匚', '入', '言', '竹', '厂', '工', '黹', '自', '片', '足', '又', '谷', '耳', '斗', '弋', '一', '巾', '瓦', '子', '夊', '鼓', '彐', '石', '夂', '禸', '八', '豆', '彡', '禾', '月', '二', '高', '黽', '鬲', '勹', '皿', '飛', '矢', '毛', '臼', '尢', '力', '网', '聿', '风', '齊', '牙', '父', '龟', '至', '巛', '魚', '疒', '彳', '血', '衣', '車', '舛', '音', '色', '丨', '舌', '斤', '厶', '鹵', '屮', '虍', '曰', '頁', '辛', '靑', '贝', '冫', '首', '糸', '匸', '食', '冖', '骨', '艮', '黃', '龜', '耒', '凵', '比', '立', '幺', '用', '十', '讠', '面', '尸', '羽', '戶', '歹', '貝', '金', '穴', '行'}

.. container:: cell code

   .. code:: python

      cql = '''
      [radical="立"]
      '''
      get_first_n(cql, 10)

   .. container:: output execute_result

      ::

         [<Concord 从立昔聲。{䇑}：短人立䇑>,
          <Concord 䇑：短人立{䇑}䇑皃。从立>,
          <Concord ：短人立䇑{䇑}皃。从立卑>,
          <Concord 屬皆从立。{䇐}：臨也。从>,
          <Concord 琳就不會有{站}在台上的我>,
          <Concord 過一個急救{站}時，我看到>,
          <Concord 級的邊沿，{站}在那裡，好>,
          <Concord 雙腿發軟，{站}著打盹，重>,
          <Concord 錢其琛下一{站}的目的地。>,
          <Concord ，你並沒有{站}在我這一邊>]

.. container:: cell markdown

   .. rubric:: 2.2 Ideographic Description Characters (IDCs)
      :name: 22-ideographic-description-characters-idcs

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

.. container:: cell code

   .. code:: python

      from CompoTree import ComponentTree
      ctree = ComponentTree.load()

      for ch in "杜李国叵":
          print(ch, ctree.ids_map.get(ch), sep=": ")

   .. container:: output stream stdout

      ::

         杜: [<⿰:木土>]
         李: [<⿱:木子>]
         国: [<⿴:囗玉>]
         叵: [<⿷:匚口>]

.. container:: cell code

   .. code:: python

      cql = '''
      [compo="木" & idc="horz2" & pos="0"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 梓。桋，赤{梀}，白者梀。>,
          <Concord 赤梀，白者{梀}。終，牛棘>,
          <Concord 謂之梁。」{梀}：短椽也。>,
          <Concord 、海楊、無{杧}；稀有長城>,
          <Concord 从木聖聲。{桺}：小楊也。>]

.. container:: cell code

   .. code:: python

      cql = '''
      [compo="木" & idc="horz2" & pos="1"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord ，寒蜩。蜓{蚞}，螇螰。蛣>,
          <Concord ，或謂之蜓{蚞}，西楚與秦>,
          <Concord ─昔者禹一{沐}而三捉髮，>,
          <Concord 吾聞之，新{沐}者必彈冠，>,
          <Concord 、饋羞、湯{沐}之饌，如他>]

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

         [<Concord 。命有司省{囹圄}，去桎梏，>,
          <Concord 修法制，繕{囹圄}，具桎梏，>,
          <Concord 廷門閭，筑{囹圄}，此所以助>,
          <Concord 加於民，而{囹圄}雖實，殺戮>,
          <Concord 。至於守司{囹圄}，禁制刑罰>]

.. container:: cell markdown

   .. rubric:: 3 Search by Phonetic Properties
      :name: 3-search-by-phonetic-properties

.. container:: cell code

   .. code:: python

      c.cql_attrs['CharPhonetic']

   .. container:: output execute_result

      ::

         {'moe': ['phon', 'tone', 'tp', 'sys="moe"'],
          '廣韻': ['攝', '聲調', '韻母', '聲母', '開合', '等第', '反切', '拼音', 'IPA', 'sys="廣韻"']}

.. container:: cell markdown

   .. rubric:: 3.1 Mandarin (based on
      `萌典 <https://github.com/g0v/moedict-data/blob/master/dict-revised.json>`__)
      :name: 31-mandarin-based-on-萌典

.. container:: cell code

   .. code:: python

      cql = '''
      [phon="ㄨㄥ" & tone="1" & sys="moe"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 哭泣不秩聲{翁}，縗絰垂涕>,
          <Concord ，黑文而赤{翁}，名曰櫟，>,
          <Concord 發猛，塤篪{翁}博，瑟易良>,
          <Concord 市朝也。而{翁}不爭焉，顧>,
          <Concord 昆吾；是使{翁}難卜於白若>]

.. container:: cell code

   .. code:: python

      cql = '''
      [phon="^pʰ" & tp="ipa" & sys="moe"] [phon="^pʰ" & tp="ipa" & sys="moe"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 之可化。志{怦怦}而內直兮，>,
          <Concord 兮何極？心{怦怦}兮諒直。皇>,
          <Concord 提到，唐文{標批}評這篇以日>,
          <Concord 轉騰潎洌，{澎濞}沆瀣，穹隆>,
          <Concord 茫，在廣漠{澎湃}的黑暗深處>]

.. container:: cell markdown

   .. rubric:: 3.2 中古漢語 (based on
      `廣韻 <https://zhuanlan.zhihu.com/p/20430939>`__)
      :name: 32-中古漢語-based-on-廣韻

.. container:: cell code

   .. code:: python

      cql = '''
      [韻母="東" & 聲調="平" & sys="廣韻"]
      '''
      get_first_n(cql, 5)

   .. container:: output execute_result

      ::

         [<Concord 堵牆，動如{風}雨，車不結>,
          <Concord 于大麓，烈{風}雷雨弗迷。>,
          <Concord 以治，四方{風}動，惟乃之>,
          <Concord ，大雷電以{風}，王逆周文>,
          <Concord 澤有九藪，{風}有八等，水>]
