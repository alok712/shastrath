# -*- coding: utf-8 -*-
"""Batch 3: extra Scholar (level 3) Vedas + Puranas so a 40 round Scholar
battle in any realm can be filled entirely with level-3 questions."""
import json, io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www", "questions.json")

NEW = [
# ------------------------------------------------------------------ VEDAS L3
("V",3,"The famous 'Earthquake Hymn' addressed to the Earth is found in which Book of the Atharvaveda?",
 ["Book 5","Book 8","Book 12","Book 20"],2,
 "पृथ्वी को संबोधित 'भूकंप सूक्त' अथर्ववेद के किस पुस्तक में मिलता है?",
 ["पुस्तक 5","पुस्तक 8","पुस्तक 12","पुस्तक 20"]),
("V",3,"How many Books (parvas) does the Atharvaveda contain?",
 ["Twelve","Eighteen","Twenty","Twenty-one"],2,
 "अथर्ववेद में कुल कितने पुस्तक (पर्व) हैं?",
 ["बारह","अठारह","बीस","इक्कीस"]),
("V",3,"The Isha Upanishad is the final chapter of which Samhita?",
 ["Vajasaneyi Samhita","Satapatha Samhita","Taittiriya Samhita","Maitrayani Samhita"],0,
 "ईश उपनिषद् किस संहिता का अंतिम अध्याय है?",
 ["वाजसनेयी संहिता","सातपथ संहिता","तैत्तिरीय संहिता","मैत्रायणी संहिता"]),
("V",3,"In Vedic studies, a 'Pratishakhya' is a supplementary text dealing with what?",
 ["Accent and pronunciation","Ritual procedure","Astronomy","Etymology"],0,
 "वैदिक अध्ययन में 'प्रतिशाख्या' किस विषय का पूरक ग्रंथ है?",
 ["उच्चारण और स्वर","यज्ञ विधि","ज्योतिष","निरुक्त"]),
("V",3,"Yaska's 'Nirukta' explains what?",
 ["The meanings and etymology of Vedic words","The ritual of the sacrifice","The stars and the zodiac","The grammar of Sanskrit"],0,
 "यासक का 'निरुक्त' किसका अर्थ और व्युत्पत्ति बताता है?",
 ["वैदिक शब्दों के अर्थ एवं व्युत्पत्ति","यज्ञ की विधि","नक्षत्र एवं राशि","संस्कृत व्याकरण"]),
("V",3,"The famous 'Hymn of the Rivers' (Nadistuti) is found in which Mandala of the Rigveda?",
 ["Mandala 1","Mandala 5","Mandala 7","Mandala 10"],2,
 "प्रसिद्ध 'नदी सूक्त' ऋग्वेद के किस मंडल में है?",
 ["मंडल 1","मंडल 5","मंडल 7","मंडल 10"]),
("V",3,"In the Rigveda, which deity is the god of healing herbs and the divine physician?",
 ["Pushan","Bhaga","Varuna","Mitra"],0,
 "ऋग्वेद में औषधियों के देवता और दैव्य चिकित्सक कौन हैं?",
 ["पूषन्","भग","वरुण","मित्र"]),
("V",3,"How many Vedangas (limbs of Vedic study) are there?",
 ["Four","Six","Eight","Twelve"],1,
 "वैदिक अंग कुल कितने माने जाते हैं?",
 ["चार","छह","आठ","बारह"]),
("V",3,"Which Upanishad begins with the famous 'Om Bhur Bhuvah Svah' invocation?",
 ["Isha Upanishad","Kena Upanishad","Katha Upanishad","Mundaka Upanishad"],0,
 "'ॐ भूर्भुवः स्वः' इस मंत्र से कौन-सा उपनिषद् आरंभ होता है?",
 ["ईश उपनिषद्","केन उपनिषद्","कठ उपनिषद्","मुण्डक उपनिषद्"]),
("V",3,"The Yama-Nachiketa dialogue of the Brihadaranyaka Upanishad teaches mainly about what?",
 ["The nature of the Atman and the path to liberation","The recitation of the Vedas","The details of the sacrifice","The origin of the cosmos"],0,
 "बृहदारण्यक उपनिषद् का यम-नचिकेता संवाद मुख्यतः किस विषय का है?",
 ["आत्मा की स्वरूपता और मोक्ष का मार्ग","वेदों का पाठ","यज्ञ का विधान","ब्रह्मांड की उत्पत्ति"]),
("V",3,"The Agni Sukta (Rigveda 1.142) praises which deity?",
 ["Agni","Indra","Varuna","Soma"],0,
 "अग्नि सूक्त (ऋग्वेद 1.142) किस देवता की स्तुति है?",
 ["अग्नि","इंद्र","वरुण","सोम"]),
("V",3,"Which numbered Sukta of the Rigveda is the famous 'Indra's Vajra' hymn?",
 ["10.90","10.129","10.130","1.142"],2,
 "ऋग्वेद का कौन-सा सूक्त प्रसिद्ध 'इन्द्रस्य वज्र' है?",
 ["10.90","10.129","10.130","1.142"]),
("V",3,"Shankaracharya's commentary on the Brahma Sutra is called what?",
 ["Brahma Sutra Bhashya","Vedanta Dipa","Gita Bhashya","Tarka Dipa"],0,
 "शकराचार्य का ब्रह्मसूत्र पर टीका किस नाम से प्रसिद्ध है?",
 ["ब्रह्मसूत्र भाष्य","वेदांत दीप","गीता भाष्य","तर्क दीप"]),
("V",3,"The earliest prose literature in Sanskrit is found in the Brahmanas of which Veda?",
 ["Rigveda","Yajurveda","Samaveda","Atharvaveda"],1,
 "संस्कृत की प्राचीनतम गद्य साहित्य किस वेद के ब्राह्मण ग्रंथों में मिलता है?",
 ["ऋग्वेद","यजुर्वेद","सामवेद","अथर्ववेद"]),
("V",3,"The famous maxim 'Tat tvam asi' (That thou art) comes from which Upanishad?",
 ["Chhandogya","Brihadaranyaka","Kena","Isha"],0,
 "'तत् त्वम् असि' यह प्रसिद्ध महावाक्य किस उपनिषद् से है?",
 ["छान्दोग्य","बृहदारण्यक","केन","ईश"]),
("V",3,"Which Vedanga deals with grammar and pronunciation rules?",
 ["Vyakarana","Kalpa","Jyotisha","Nirukta"],0,
 "कौन-सा वेदांग व्याकरण और उच्चारण नियमों से संबंधित है?",
 ["व्याकरण","कल्प","ज्योतिष","निरुक्त"]),
# ---------------------------------------------------------------- PURANAS L3
("P",3,"The Padma Purana is attributed to which sage?",
 ["Lomapada (Utanka)","Vyasa","Parashara","Markandeya"],0,
 "पद्म पुराण का श्रेय किस ऋषि को दिया जाता है?",
 ["लोमपाद (उतंक)","व्यास","पराशर","मार्कण्डेय"]),
("P",3,"Which Purana contains the famous philosophical section on Shankaracharya?",
 ["Markandeya Purana","Garuda Purana","Brahmanda Purana","Vamana Purana"],0,
 "शंकराचार्य पर प्रसिद्ध दार्शनिक अध्याय किस पुराण में है?",
 ["मार्कण्डेय पुराण","गरुड़ पुराण","ब्रह्माण्ड पुराण","वामन पुराण"]),
("P",3,"Which Purana tells of King Bhagiratha and the descent of the river Ganga?",
 ["Brahmanda Purana","Garuda Purana","Skanda Purana","Matsya Purana"],0,
 "राजा भगीरथ और गंगा के अवतरण की कथा किस पुराण में है?",
 ["ब्रह्माण्ड पुराण","गरुड़ पुराण","स्कन्द पुराण","मत्स्य पुराण"]),
("P",3,"The Vamana Purana contains the famous genealogy of which royal lineage?",
 ["The Solar dynasty (Suryavamsha)","The Lunar dynasty (Chandravamsha)","The Ikshvaku dynasty","The Yadava dynasty"],0,
 "वामन पुराण में किस राजवंश की प्रसिद्ध वंशावली मिलती है?",
 ["सूर्यवंश","चंद्रवंश","इक्ष्वाकुवंश","यादववंश"]),
("P",3,"Which Purana describes the realm of Yama and the judgement of the dead?",
 ["Garuda Purana","Brahma Purana","Skanda Purana","Padma Purana"],0,
 "यम के लोक और मृतकों के न्याय का वर्णन किस पुराण में है?",
 ["गरुड़ पुराण","ब्रह्म पुराण","स्कन्द पुराण","पद्म पुराण"]),
("P",3,"Which Purana gives the classical 'Mahattattva' (five elements) doctrine of the elements and the Purusha-Prakriti philosophy?",
 ["Bhagavata Purana","Garuda Purana","Vamana Purana","Matsya Purana"],0,
 "पंच महाभूत और पुरुष-प्रकृति दर्शन का शास्त्रीय वर्णन किस पुराण में है?",
 ["भागवत पुराण","गरुड़ पुराण","वामन पुराण","मत्स्य पुराण"]),
("P",3,"The Durga Saptashati is traditionally recited during which festival?",
 ["Navaratri","Maha Shivaratri","Holi","Kumbh Mela"],0,
 "दुर्गा सप्तशती का पाठ परंपरागत रूप से किस त्योहार के दौरान होता है?",
 ["नवरात्रि","महाशिवरात्रि","होली","कुंभ मेला"]),
("P",3,"How many Manvantaras (cosmic ages) are described in the Vishnu Purana?",
 ["Seven","Ten","Fourteen","Fifteen"],2,
 "विष्णु पुराण में कितने मन्वन्तर वर्णित हैं?",
 ["सात","दस","चौदह","पंद्रह"]),
("P",3,"In the traditional list of the eighteen Mahapuranas, which Purana is the tenth and is named after the son of Shiva?",
 ["Skanda Purana","Markandeya Purana","Agni Purana","Brahma Purana"],0,
 "अठारह महापुराणों की पारंपरिक सूची में दसवाँ पुराण कौन-सा है जो शिव के पुत्र के नाम पर है?",
 ["स्कन्द पुराण","मार्कण्डेय पुराण","अग्नि पुराण","ब्रह्म पुराण"]),
("P",3,"In the traditional list of the eighteen Mahapuranas, which Purana is the twelfth and is named after the fire god?",
 ["Agni Purana","Skanda Purana","Markandeya Purana","Vamana Purana"],0,
 "अठारह महापुराणों की पारंपरिक सूची में बारहवाँ पुराण अग्नि के नाम पर कौन-सा है?",
 ["अग्नि पुराण","स्कन्द पुराण","मार्कण्डेय पुराण","वामन पुराण"]),
("P",3,"In the traditional list of the eighteen Mahapuranas, which Purana is the sixth and is named after the fish avatar?",
 ["Matsya Purana","Vamana Purana","Garuda Purana","Kurma Purana"],0,
 "अठारह महापुराणों की पारंपरिक सूची में छठा पुराण मत्स्य अवतार के नाम पर कौन-सा है?",
 ["मत्स्य पुराण","वामन पुराण","गरुड़ पुराण","कूर्म पुराण"]),
("P",3,"In the traditional list of the eighteen Mahapuranas, which Purana is the fifteenth and is named after the tortoise avatar?",
 ["Kurma Purana","Matsya Purana","Varaha Purana","Brahmanda Purana"],0,
 "अठारह महापुराणों की पारंपरिक सूची में पंद्रहवाँ पुराण कूर्म अवतार के नाम पर कौन-सा है?",
 ["कूर्म पुराण","मत्स्य पुराण","वराह पुराण","ब्रह्माण्ड पुराण"]),
("P",3,"In the traditional list of the eighteen Mahapuranas, which Purana is the eighth?",
 ["Brahmanda Purana","Brahmavaivarta Purana","Garuda Purana","Matsya Purana"],0,
 "अठारह महापुराणों की पारंपरिक सूची में आठवाँ पुराण कौन-सा है?",
 ["ब्रह्माण्ड पुराण","ब्रह्मवैवार्त पुराण","गरुड़ पुराण","मत्स्य पुराण"]),
("P",3,"In the traditional list of the eighteen Mahapuranas, which Purana is the ninth?",
 ["Brahmavaivarta Purana","Skanda Purana","Brahmanda Purana","Agni Purana"],0,
 "अठारह महापुराणों की पारंपरिक सूची में नववाँ पुराण कौन-सा है?",
 ["ब्रह्मवैवार्त पुराण","स्कन्द पुराण","ब्रह्माण्ड पुराण","अग्नि पुराण"]),
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
