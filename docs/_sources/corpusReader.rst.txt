Corpus Input
============

:class:`dcctk.corpusReader.PlainTextReader` deals with the default plain text 
corpus structure input in :code:`dcctk`.
To read in corpus with other structures, you could write your own class or 
function that returnes a corpus object that follows the required structure. 
This required structure can be found below (a corpus with two timesteps, with 
each timestep having three texts in it):

.. code-block:: json
    :caption: Required corpus structure

    [
       {
          "id": "01",
          "m": {"label": "1st timestep", "ord": 1, "time_range": [-1000, -206]},
          "text": [
              {
                  "c": ["這是第三篇裡的一個句子。", "這是第二個句子。"],
                  "id": "01/text3.txt",
                  "m": {"about": "Text 3 in 1st timestep"}
              },
              {
                  "c": ["這是一個句子。", "這是第二個句子。"],
                  "id": "01/text1.txt",
                  "m": {"about": "Text 1 in 1st timestep"}
              },
              {
                  "c": [
                      "這是第二篇裡的一個句子。", "這是第二個句子。"],
                  "id": "01/text2.txt",
                  "m": {"about": "Text 2 in 1st timestep"}
              }
          ]
       },
       {
          "id": "02",
          "m": {"label": "2nd timestep", "ord": 2, "time_range": [-205, 220]},
          "text": [
              {
                  "c": ["這是第三篇裡的一個句子。", "這是第二個句子。"],
                  "id": "02/text3.txt",
                  "m": {"about": "Text 3 in 2nd timestep"}
              },
              {
                  "c": ["這是一個句子。", "這是第二個句子。"],
                  "id": "02/text1.txt",
                  "m": {"about": "Text 1 in 2nd timestep"}
              },
              {
                  "c": ["這是第二篇裡的一個句子。", "這是第二個句子。"],
                  "id": "02/text2.txt",
                  "m": {"about": "Text 2 in 2nd timestep"}
              }
          ]
       }    
    ]

.. autoclass:: dcctk.corpusReader.PlainTextReader
    :members:
    :special-members: 

.. automodule:: dcctk.UtilsTextProcess
    :members:
    :undoc-members:
