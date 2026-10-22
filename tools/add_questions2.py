# -*- coding: utf-8 -*-
"""Batch 2: extra Scholar (level 3) Vedas + Puranas riddles so that 40-round
Scholar matches never have to fall back to easier questions."""
import json, io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www", "questions.json")

NEW = [
("V",3,"In which Mandala and Sukta of the Rigveda does the famous 'Hymn of the Frogs' appear?",
 ["Mandala 1, Sukta 1","Mandala 7, Sukta 85","Mandala 9, Sukta 1","Mandala 10, Sukta 85"],1,
 "ऋग्वेद के किस मंडल और सूक्त में प्रसिद्ध 'मंडूक सूक्त' पाया जाता है?",
 ["मंडल 1, सूक्त 1","मंडल 7, सूक्त 85","मंडल 9, सूक्त 1","मंडल 10, सूक्त 85"]),
("V",3,"How many Upanishads are counted in the canonical Muktika list?",
 ["100","108","110","120"],1,
 "मुक्तिका सूची में कुल कितने उपनिषद् गिने जाते हैं?",
 ["100","108","110","120"]),
("V",3,"The famous dialogue between Uddalaka and Shvetaketu is found in which Upanishad?",
 ["Chhandogya","Brihadaranyaka","Kena","Isha"],0,
 "उद्दालक और श्वेतकेतु का प्रसिद्ध संवाद किस उपनिषद् में है?",
 ["छान्दोग्य","बृहदारण्यक","केन","ईश"]),
("V",3,"How many verses does the Kena Upanishad contain?",
 ["Four","Six","Eight","Twelve"],0,
 "केन उपनिषद् में कितने मंत्र हैं?",
 ["चार","छह","आठ","बारह"]),
("V",3,"The Aitareya Brahmana belongs to which Veda?",
 ["Rigveda","Yajurveda","Samaveda","Atharvaveda"],0,
 "ऐतरेय ब्राह्मण किस वेद का ग्रंथ है?",
 ["ऋग्वेद","यजुर्वेद","सामवेद","अथर्ववेद"]),
("V",3,"How many Upanishads belong to the Shukla (White) Yajurveda?",
 ["One","Two","Three","Four"],1,
 "शुक्ल (श्वेत) यजुर्वेद से कितने उपनिषद् संबद्ध हैं?",
 ["एक","दो","तीन","चार"]),
("V",3,"How many Upanishads belong to the Krishna Yajurveda?",
 ["Two","Three","Four","Six"],2,
 "कृष्ण यजुर्वेद से कितने उपनिषद् संबद्ध हैं?",
 ["दो","तीन","चार","छह"]),
("V",3,"The Devi Suktam is which numbered Sukta of the Rigveda?",
 ["10.85","10.90","10.129","10.71"],0,
 "देवी सूक्त ऋग्वेद का कौन-सा सूक्त है?",
 ["10.85","10.90","10.129","10.71"]),
("V",3,"The Nasadiya Sukta (Hymn of Creation) is found in which Mandala of the Rigveda?",
 ["Mandala 1","Mandala 5","Mandala 8","Mandala 10"],3,
 "नासदीय सूक्त (सृष्टि सूक्त) ऋग्वेद के किस मंडल में है?",
 ["मंडल 1","मंडल 5","मंडल 8","मंडल 10"]),
("V",3,"Which Samhita is the Taittiriya recension of the Krishna Yajurveda?",
 ["Taittiriya Samhita","Maitrayani Samhita","Kanva Samhita","Satapatha Samhita"],0,
 "कृष्ण यजुर्वेद की तैत्तिरीय शाखा कौन-सी संहिता है?",
 ["तैत्तिरीय संहिता","मैत्रायणी संहिता","काण्व संहिता","सातपथ संहिता"]),
# ------------------------------------------------------------------ PURANAS L3
("P",3,"Which Purana contains the Dakshayana Yajna and the self-immolation of Sati?",
 ["Markandeya Purana","Vamana Purana","Brahmanda Purana","Garuda Purana"],0,
 "दक्ष यज्ञ और सती के सहज्या वर्णन किस पुराण में हैं?",
 ["मार्कण्डेय पुराण","वामन पुराण","ब्रह्माण्ड पुराण","गरुड़ पुराण"]),
("P",3,"How many verses does the extended (13,500-verse) version of the Devi Mahatmya contain?",
 ["1,350","7,000","13,500","21,000"],2,
 "देवी माहात्म्य के विस्तृत (13,500 मंत्र) रूप में कितने मंत्र हैं?",
 ["1,350","7,000","13,500","21,000"]),
("P",3,"The famous 'Brahma Yamuna' story is found in which Purana?",
 ["Brahmanda Purana","Garuda Purana","Padma Purana","Markandeya Purana"],0,
 "प्रसिद्ध 'ब्रह्म-यमुना' कथा किस पुराण में मिलती है?",
 ["ब्रह्माण्ड पुराण","गरुड़ पुराण","पद्म पुराण","मार्कण्डेय पुराण"]),
("P",3,"The famous 'Nagarakshasa' section on the duties of kings is found in which Purana?",
 ["Garuda Purana","Skanda Purana","Markandeya Purana","Vamana Purana"],0,
 "राजधर्म पर विस्तृत 'नागरक्षस' अध्याय किस पुराण में है?",
 ["गरुड़ पुराण","स्कन्द पुराण","मार्कण्डेय पुराण","वामन पुराण"]),
("P",3,"Although counted among the eighteen Puranas, the Harivamsa is a supplement to which great epic?",
 ["The Mahabharata","The Ramayana","The Bhagavata Purana","The Harishchandra"],0,
 "अठारह पुराणों में गिने जाने पर भी हरिवंश किस महाकाव्य का परिशिष्ट है?",
 ["महाभारत","रामायण","भागवत पुराण","हरिश्चन्द्र"]),
("P",3,"Which Purana tells of Vishnu as the dwarf who asks for three feet of land?",
 ["Vamana Purana","Garuda Purana","Matsya Purana","Kurma Purana"],0,
 "तीन पाद भूमि माँगने वाले विघन के रूप में विष्णु का वर्णन किस पुराण में है?",
 ["वामन पुराण","गरुड़ पुराण","मत्स्य पुराण","कूर्म पुराण"]),
("P",3,"Which Purana tells of the boar avatar lifting the earth out of the ocean?",
 ["Varaha Purana","Matsya Purana","Kurma Purana","Garuda Purana"],0,
 "समुद्र से पृथ्वी उठाने वाले वराह अवतार का वर्णन किस पुराण में है?",
 ["वराह पुराण","मत्स्य पुराण","कूर्म पुराण","गरुड़ पुराण"]),
("P",3,"Which Purana tells of Krishna lifting Mount Govardhan on his little finger?",
 ["Bhagavata Purana","Vishnu Purana","Brahmanda Purana","Padma Purana"],0,
 "कृष्ण द्वारा अपनी उंगली पर गोवर्धन पर्वत उठाने का वर्णन किस पुराण में है?",
 ["भागवत पुराण","विष्णु पुराण","ब्रह्माण्ड पुराण","पद्म पुराण"]),
("P",3,"The Devi Purana (Durga Saptashati) is a section of which great Purana?",
 ["Markandeya Purana","Brahma Purana","Skanda Purana","Vamana Purana"],0,
 "देवी पुराण (दुर्गा सप्तशती) किस महान पुराण का अंग है?",
 ["मार्कण्डेय पुराण","ब्रह्म पुराण","स्कन्द पुराण","वामन पुराण"]),
("P",3,"H. H. Wilson's famous English translation of the Vishnu Purana was published in which year?",
 ["1812","1840","1887","1905"],1,
 "एच. एच. विल्सन का विष्णु पुराण का प्रसिद्ध अंग्रेज़ी अनुवाद किस वर्ष प्रकाशित हुआ?",
 ["1812","1840","1887","1905"]),
]

def main():
    with io.open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    existing = data["questions"]
    seen = {(q.get("epic"), q.get("q")) for q in existing}
    added = 0
    for epic, lvl, q, opts, ans, hq, hopts in NEW:
        if (epic, q) in seen:
            continue
        assert len(opts) == 4 and len(hopts) == 4 and ans in (0, 1, 2, 3), q
        existing.append({"epic": epic, "level": lvl, "q": q, "options": list(opts), "answer": ans,
                          "tr": {"hi": {"q": hq, "options": list(hopts)}}})
        seen.add((epic, q))
        added += 1
    with io.open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("Added %d questions. Total now %d." % (added, len(existing)))

if __name__ == "__main__":
    main()
