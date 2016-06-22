# Copyright 2016 Mario Graff (https://github.com/mgraffg)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def test_tweet_iterator():
    import os
    import gzip
    from b4msa.utils import tweet_iterator
    
    fname = os.path.dirname(__file__) + '/text.json'
    a = [x for x in tweet_iterator(fname)]
    fname_gz = fname + '.gz'
    with open(fname, 'r') as fpt:
        with gzip.open(fname_gz, 'w') as fpt2:
            fpt2.write(fpt.read().encode('ascii'))
    b = [x for x in tweet_iterator(fname_gz)]
    assert len(a) == len(b)
    for a0, b0 in zip(a, b):
        assert a0['text'] == b0['text']
    os.unlink(fname_gz)


def test_textmodel():
    from b4msa.textmodel import TextModel
    from b4msa.utils import tweet_iterator
    import os
    fname = os.path.dirname(__file__) + '/text.json'
    tw = list(tweet_iterator(fname))
    text = TextModel([x['text'] for x in tw])
    # print(text.tokenize("hola amiguitos gracias por venir :) http://hello.com @chanfle"))
    # assert False
    assert isinstance(text[tw[0]['text']], list)


def test_params():
    import os
    import itertools
    from b4msa.params import BASIC_OPTIONS
    from b4msa.textmodel import TextModel
    from b4msa.utils import tweet_iterator

    params = dict(strip_diac=[True, False], usr_option=BASIC_OPTIONS,
                  url_option=BASIC_OPTIONS)
    params = sorted(params.items())
    fname = os.path.dirname(__file__) + '/text.json'
    tw = [x for x in tweet_iterator(fname)]
    text = [x['text'] for x in tw]
    for x in itertools.product(*[x[1] for x in params]):
        args = dict(zip([x[0] for x in params], x))
        ins = TextModel(text, **args)
        assert isinstance(ins[text[0]], list)

def test_emoticons():
    from b4msa.textmodel import EmoticonClassifier, norm_chars
    emo = EmoticonClassifier()
    for a, b in [
            ("Hi :) :P XD", "~Hi~_pos~_pos~_pos~"),
            ("excelente dia xc", "~excelente~dia~_neg~")
    ]:
        _a = norm_chars(a)
        assert ' ' not in _a, "norm_chars normalizes spaces {0} ==> {1}".format(a, _a)
        _b = emo.replace(_a)
        print("[{0}] => [{1}]; should be [{2}]".format(a, _b, b))
        assert _b == b


def test_lang():
    from b4msa.textmodel import TextModel

    text = [
        "Hi :) :P XD",
        "excelente dia xc",
        "el alma de la fiesta XD"
    ]
    model = TextModel(text, **{
        "del_dup1": True,
        "emo_option": "group",
        "lc": True,
        "negation": True,
        "num_option": "group",
        "stemming": True,
        "stopwords": "group",
        "strip_diac": False,
        "token_list": [
            -1,
            # 5,
        ],
        "url_option": "group",
        "usr_option": "group",
        "lang": "spanish",
    })
    a = model.tokenize("El alma de la fiesta :) conociendo la maquinaria @user bebiendo nunca manches que onda")
    assert a == ['_sw', 'alma', '_sw', '_sw', 'fiest', '_pos', 'conoc', '_sw', 'maquinari', '_usr', 'beb', 'no', 'manch', '_sw', 'onda']

