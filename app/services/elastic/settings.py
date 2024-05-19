SETTINGS = {
    "settings": {
        "index": {
            "analysis": {
                "filter": {
                    "my_phonetic_cyrillic": {
                        "type": "phonetic",
                        "encoder": "beider_morse",
                        "rule_type": "approx",
                        "name_type": "generic",
                        "languageset": "cyrillic"
                    },
                    "my_phonetic_english": {
                        "type": "phonetic",
                        "encoder": "beider_morse",
                        "languageset": "english",
                        "rule_type": "approx",
                        "name_type": "generic"
                    },
                },
                "analyzer": {
                    "phoneticAnalyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "my_phonetic_english", "my_phonetic_cyrillic"]
                    },
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "id": {
                "type": "long"
            },
            "name_normalized": {
                "type": "text",
                "analyzer": "phoneticAnalyzer"
            }
        }
    }
}
