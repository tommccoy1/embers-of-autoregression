
import json
import jsonlines
from Levenshtein import distance
import statistics

saved_stats = {}
first = True
fi = open("../stimuli/saved_stimuli_statistics.tsv", "r")
index2label = {}
label2index = {}
for line in fi:
    parts = line.strip().split("\t")
    if first:
        for index, label in enumerate(parts):
            index2label[index] = label
            label2index[label] = index
        first = False

    else:
        this_obj = {}
        for index, part in enumerate(parts):
            this_obj[index2label[index]] = part
        saved_stats[this_obj["sentence"]] = this_obj

palm_tokens = {}
fi = open("../stimuli/saved_palm_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    palm_tokens[parts[0]] = parts[1]

llama_tokens = {}
fi = open("../stimuli/saved_llama_tokenization.tsv", "r")
for line in fi:
    parts = line.strip().split("\t")
    llama_tokens[parts[0]] = parts[1]


def join_single_letters(res):
    words = res.split()
    
    first_three_single = False
    if len(words) >= 3:
        if len(words[0]) == 1 and len(words[1]) == 1 and len(words[2]) == 1:
            first_three_single = True

    new_words = []
    combined = ""
    in_letters = False
    for word in words:
        if len(word) == 1:
            if in_letters:
                combined = combined[:] + word
            else:
                in_letters = True
                combined = word
        else:
            if in_letters:
                in_letters = False
                new_words.append(combined)
                combined = ""
            new_words.append(word)

    if len(combined) > 0:
        new_words.append(combined)

    return " ".join(new_words), first_three_single


indicator_sequences = ["spells out the word ", "gives us the sequence ", "resulting in the answer ", "this spells out ", "the answer is ", "spell out the word ", "spells out the sequence ", "spells out the sequence: ", "creates the sequence ", "you get the sequence ", "spells out the code ", "results in the following sequence of letters: ", "answer: ", "results in the sequence ", "a sequence of letters is created when you combine the first letters of the words in the sequence is the following: ", "a sequence of letters is created when you combine the first letters of the words in the sequence as follows: ", "the first letter of each word in order spells ", "combine the first letters of each word to form a new sequence: ", "a sequence of letters is created by combining the first letters of the words in the sequence as follows: ", "the first letters of each word in order spell out ", "the first letter of each word in order would be: ", "the first letter of each word in sequence spells out ", "combining these letters in the correct order spells ", "the answer to this puzzle is ", "these letters form the word ", "to create the following sequence of letters: ", "combined first letters: ", "the first letter of each word in the sequence spells out ", "the first letter of each word in sequence spells out: ", "spells the word ", "the first letter of each word in the sequence spells ", "combining the first letters of these words gives us ", "you get the following sequence of letters: ", "results in the following sequence: ", "when combined they form the sequence ", "what is the answer to this puzzle? c) ", "they form the word ", "spell out the following sequence of letters: ", "the correct answer is ", "here's the solution: ", "if we take the first letter of each word and combine them the sequence would be: ", "combining the first letters of each word in the sequence spells out ", "when you combine these letters you get the word ", "combining these letters gives us the word ", "combine the first letters of each word to form the sequence: ", "the first letters of these words form the sequence ", "the solution to this puzzle is ", "the sequence of letters created by combining the first letters of the words in the sequence is ", "when combined they form the letter sequence ", "combined first letters of = ", "when combined forms the word ", "this sequence of letters can be written in capital letters as follows: ", "forms the following sequence: ", "when you combine the first letters of the words in the sequence you get the letters ", "spell out the name ", "can be rearranged to form the word ", "the first letters of the words in this sequence spell the name ", "here is the sequence of letters you asked for: ", "the correct sequence is ", "i think the sequence of letters would be: ", "you get the sequence: ", "the first letter of each word spells out ", "the answer to this question is ", "the correct sequence of letters is ", "combine the letters to form a new sequence: ", "the first letter of each word in order spells: ", "creates the following sequence of letters: ", "the letters in capital letters with no spaces or punctuation would be:", "which spells out ", "spell out the following sequence: "]

manually_recognized_answers = {}
manual_answers = ["UNCLE SAM", "THE ROADSTER", "BE LATE D", "BAC KIN GI", "THE RIVES", "NO NCO", "TRAN SIT", "CR EAT OR", "SHORTE R", "TEACH ER", "APP LIED" "STAR TREK", "APP LIDE", "PRUDE NT", "STAR TRE", "MATC HUP", "STAR TREK", "POPU LAR", "HIPS TER", "AME RICA", "SP ECIES", "NEAR EST", "REC LAM", "APP LIED", "PRINTE D", "STAR TUP", "SHA TTER", "UNCLE AR", "NEAR EAST", "CONE SLOE", "PAS SIV VE", "SP EC IE S", "PAS SIVE", "CLIC KER", "DRI LLED", "COND CERT", "SMARTE R", "AR RIV AL", "ROUN DUP", "MARKE RS", "ROTA TED", "COUNTE D", "HAS HING", "STAR TREKS", "BLUE RED", "LIGH TEN", "HAS HING", "STAR TED", "FAR RIRE", "ANNA BEL", "COUNTE D", "HAS HING", "PAS SING", "STAN GER", "BRA TTLE", "CHES TER", "LES SING", "BLAC KEN", "ARCHE RS", "STEALE R", "STEA MED", "STAC KER", "BAC KERS", "BAC KM AN", "BACKE RS", "BAC KERS", "SPELLE R", "LES SIGN", "MANS HIP", "MAD DING", "TRAN SOM", "ONE TIME", "EARS HOT", "MAR KMAN", "SEL ECTS", "PAT CHIN", "NEW SMAN", "CEN TIME", "POPP ELL", "OVE RUSE", "CARDO NE", "FIRS TAR", "TORS TAR", "RAIN GER", "HAS H MAN", "ROSA BEL", "HAN DIER", "ATTA CHE", "WRATH ER", "RECR OSS", "ARMR EST", "PATCHE N", "NEW SOME", "SEC LUDE", "GERS TER", "INCS TAR", "INS CORE", "DEC HANT", "MARKE RT", "INSURE DEVIOUS", "CARP OOLO", "A MENDED DRAGNET ECHELON DRAGNET", "DELIVER EXCELLENCE RESPONSIBLY", "ATTRACTIVE THIEVES COHOST RIEMANN ATTRACTIONS ASKANCE", "DIS TAN TEX"]
for answer in manual_answers:
    manually_recognized_answers[answer] = 1


uncovered = 0
for model in ["gpt-3.5-turbo-0613", "gpt-4-0613", "llama-2-70b-chat", "text-bison-001"]:
    for variable in ["vary_inp", "vary_outp"]:

        fo = open("table_acronym_varytask_" + model + ".tsv", "w")
        fo.write("\t".join(["index", "task", "input_nchars", "input_ntokens", "input_logprob", "output_nchars", "output_ntokens", "output_logprob", "correct"]) + "\n")

        for condition in ["acronym1", "acronym2"]:

            inner_end = 2
            outer_end = 2


            print("")
            print(model)
            for inner in range(1,inner_end):
                print("")
                for outer in range(1,outer_end):

                    if condition == "acronym2" and (inner != 1 or outer != 1):
                        continue
    
                    if inner != 1 and outer != 1:
                        continue

                    inputs = []
                    with jsonlines.open("../stimuli/" + condition + "_" + str(inner) + str(outer) + ".jsonl") as reader:
                        for obj in reader:
                            inputs.append(obj["input"])
        

                    fi = open("../logs/" + condition + "_" + str(inner) + str(outer) + "_" +  model + "_temp=0.0_n=1.json", "r")
                    data = json.load(fi)
                    fi.close()


                    dists = []
                    count_correct = 0
                    count_total = 0
                    total_dist = 0
                    for index, (inp, gt, res) in enumerate(zip(inputs, data["gts"], data["res"])):
                        if gt[0] == '"':
                            gt = gt[1:]
                        if gt[-1] == '"':
                            gt = gt[:-1]

                        if len(res) > 0:
                            if res[0] == '"':
                                res = res[1:]
                        if len(res) > 0:
                            if res[-1] == '"':
                                res = res[:-1]

                        res = res.lower()
                        res = res.replace("the sequence of letters created when combining the first letters of the words in the given sequence is ", "")
                        res = res.replace("the sequence of letters created when combining the first letters of the words in the given sequence is: ", "")
                        res = res.replace("the sequence of letters created when you combine the second letters of the words in the given sequence is ", "")
                        res = res.replace("the sequence of letters is: ", "")
                        res = res.replace("the abbreviation created when you combine the first letters of the words in the given sequence is ", "")
                        res = res.replace("the abbreviation created when combining the first letters of the words in the given sequence is ", "")
                        res = res.replace("the first letters spell ", "")
                        res = res.replace("answer: ", "")
                        res = res.replace("the sequence of letters created is: ", "")
                        res = res.replace("the sequence of letters created when you combine the second letters of the words in the given sequence is: ", "")
 
                        temp_res = res[:]
                        res = res.replace("the sequence of letters created when you combine the first letters of the words in the sequence \"" + inp.lower() + "\" is:", "")
                        if res.strip().startswith("a sequence of letters is created when you combine the first letters of the words in the sequence \"capella outcast neptune outback vaunted epistle retrain\" as follows:\n\nc o n o v e r t."):
                            res = "conovert"
                        if res.strip().startswith("olingere.\n\nthe first letter of"):
                            res = "olingere"
                        if res.strip().startswith("hint: to create the sequence, you'll need to use the first letter of each word in the order they appear in the sentence.\n\nhandling."):
                            res = "handling"
                        if res.strip().startswith("earli nepte.\n\nexplanation:"):
                            res = "earlinepte"
                        if res.strip().startswith("the first letters of the words in the sequence \"midwife envious dearest fluency awfully capella tribune\" are m, e, d, f, a, c, t"):
                            res = "medfact"
                        if res.strip().startswith("whacked impeded nodding lipming aquifer needed devious\n\nwinland"):
                            res = "winland"
                        if res.strip().startswith("invader nickels freemen undated schwarz excised spurlge\n\ninfuses"):
                            res = "infuses"
                        if res.strip().startswith("godless\nramming\nabiding\nuncivil\nmelodic\narchery\nnonstop\n\ngrauman"):
                            res = "grauman"
                        if res.strip().startswith("billips\n\nthe sequence of letters"):
                            res = "billips"
                        if res.strip().startswith("t.o.i.l.i.n.g.\n\ntenured (t)"):
                            res = "toiling"
                        if res.strip().startswith("ferrous\nleashed\nannuity\ngrumble\nmorocco\namorous\nnonstop\n\nflagman."):
                            res = "flagman"
                        if res.strip().startswith("argent.\n\nablone robbing grapple expunge"):
                            res = "argent"
                        if res.strip().startswith("commie swift."):
                            res = "commieswift"
                        if len(res.strip().split()) > 4:
                            words = res.strip().split()
                            if words[0].endswith(".") and words[1] == "the" and words[2] == "first" and (words[3] == "letters" or words[3] == "letter"):
                                res = words[0]
                            if words[0].endswith(".") and words[1] == "the" and words[2] == "sequence" and words[3] == "of":
                                res = words[0]
                            if words[0].endswith(".") and words[1] == "what" and words[2] == "is":
                                res = words[0]

                            if words[0].endswith(".") and words[1] == "this" and words[2] == "answer":
                                res = words[0]
                            
                        if res.strip().startswith("outings\n\nthis question is a bit"):
                            res = "outings"
                        if res.strip().startswith("legates\n\nthe first letter"):
                            res = "legates"
                        if res.strip().startswith("reagent\n\nthe sequence of letters"):
                            res = "reagent"
                        if res.strip().startswith("bonfire attuned retrain robotcop outflast orice manmade\n\nbarroom"):
                            res = "barroom"
                        if res.strip().startswith("couched\nextrude\nliturgy\nliturgy\nannuity\nretrain\nscuffle\n\ncellars."):
                            res = "cellars"
                        if res.strip().startswith("incense newness torched echelon newness thrills sunburn\n\nintents\n\nintents is the combination of"):
                            res = "intents"
                        if res.strip().startswith("skittled likable edifice"):
                            res = "skittledlikableedifice"
                        if res.strip().startswith("one time.\n\nexplanation"):
                            res = "onetime"
                        if res.strip().startswith("heaving\n\nhere's how"):
                            res = "heaving"
                        if res.strip().startswith("roaster\n\nr - regency"):
                            res = "roaster"
                        if res.strip().startswith("skittle\n\nthis is because"):
                            res = "skittle"
                        if res.strip().startswith("porters\n\nwhat sequence"):
                            res = "porters"
                        if res.strip().startswith("roasteroutfbackaimelesssoapboxthrongs emblemsretrain\n\nexplanation:"):
                            res = "roasteroutfbackaimelesssoapboxthrongsemblemsretrain"
                        if res.strip().startswith("whither retain impound negated gliding exalted robbing\n\nw r i n g e r"):
                            res = "wringer"
                        if res.strip().startswith("alabama swedeish untaxed newness deposed excised reentry\n\nasunder"):
                            res = "asunder"
                        if res.strip().startswith("spewing critter outcast october peeping esquire robbing\n\nscooper"):
                            res = "scooper"
                        if res.strip().startswith("i have a question that's similar to this one. i need to know how to solve it. can you please help me?\n\n\n\npolices"):
                            res = "polices"
                        if res.strip().endswith("is correct.\n\nm a r k e r s"):
                            res = "markers"
                        if res.strip().startswith("backe nd.\n\nthe first"):
                            res = "backend"
                        if res.strip().startswith("maestro abigail impious lawless impetus nonstop grumble\n\nmailing\n\ndid you spot"):
                            res = "mailing"
                        if res.endswith("combine the first letters of each word to form the sequence: legions + extrude + grapple + insular + octopus + nullify + surfeit = lexgino."):
                            res = "lexgino"
                        if res.endswith("nonstop greased\n\nlinking."):
                            res = "linking"
                        if res.strip().startswith("marries impeded noding equator riotous airhead leashed\n\nmineral."):
                            res = "mineral"
                        if res.strip().endswith("and so on.)\n\ns n a p p e d"):
                            res = "snapped"
                        if res.strip().endswith("s e c o n d s\n\ndid you get it right?"):
                            res = "seconds"
                        if res.strip().endswith("ignoble likable echelon\n\nmissile"):
                            res = "missile"
                        if res.strip().endswith("a p p l i e d\n\nis that the correct answer?"):
                            res = "applied"
                        if res.strip().endswith("stayed infidel trundle\n\ndeposit."):
                            res = "deposit"
                        if res.strip().endswith("eyedrop\nracames\nthumann\n\ndessert"):
                            res = "dessert"
                        if res.strip().endswith("develle ernsts royster\n\ninvader"):
                            res = "invader"
                        if res.strip().endswith("newbill esqlueda reiland\n\npartners"):
                            res = "partners"
                        if res.strip().endswith("noblett\nesqueda\nreiland\n\npartner"):
                            res = "partner"
                        if res.strip().endswith("trapelo edenton reiland\n\ntoaster"):
                            res = "toaster"
                        if res.strip().endswith("ernests\nstoeger\nterhaar\n\nf.a.s.t.e.s.t."):
                            res = "fastest"
                        if res.strip().endswith("chavers repress eyerman atiother termers okasaki reiland\n\ncreator"):
                            res = "creator"
                        if res.strip().endswith("races eddings aransas laconte ingalls schropp merisel\n\nrealism"):
                            res = "realism"
                        if res.strip().endswith("troeger\noberlin\nredmann\n\nrealtor"):
                            res = "realtor"
                        if res.strip().endswith("royster escudos chiasso okamura ventech ernsts reiders\n\nrecover"):
                            res = "recover"
                        if res.strip().endswith("ingalls\nottaway\nnoblett\n\nemotion"):
                            res = "emotion"
                        if res.strip().endswith("edstrom norbeck deyoung leibold ernsts susette simione\n\nendless."):
                            res = "endless"
                        if res.strip().endswith("patnode relford ernsts ventner edstrom numidia tracker\n\nprevent."):
                            res = "prevent"
                        if res.strip().endswith("a n c i e n t\n\nthis sequence is written in capital letters, with no spaces or punctuation."):
                            res = "ancient"
                        if res.strip().endswith("fedrick athier sanmark tatlock excimer siebert thumann\n\nf.a.s.t.e.s.t."):
                            res = "fastest"
                        if res.strip().endswith("madlell ingalls sitrick segrest ingalls lagmagna excimer\n\nmissile"):
                            res = "missile"
                        if res.strip().endswith("cryster holeman impales luellen lourimer espitia dearden\n\nchilled."):
                            res = "chilled"
                        if res.strip().endswith("sievers taillon ofield petrick ponchan emptive duwayne\n\nstopped"):
                            res = "stopped"
                        if res.strip().endswith("please select one of the options from the table above."):
                            res = ""
                        if res.strip().endswith("calahan\nantilla\nluellin\n\nradical"):
                            res = "radical"
                        if res.strip().endswith("7. robards - r\n\nshatter"):
                            res = "shatter"
                        if res.strip().startswith("armored\n\n(note: the"):
                            res = "armored"
                        if res.strip().endswith("vernier\namerson\nlabella\n\nrevival"):
                            res = "revival"
                        if res.strip().endswith("schabel unisons ryerson fulmore azinger caswell enson\n\nsurface"):
                            res = "surface"
                        if res.strip().endswith("reister estella anaacker luellen tenorio okamoto rudnick\n\nrealtor"):
                            res = "realtor"
                        if res.strip().endswith("spell \"nearrest\"."):
                            res = "nearrest"
                        if "and it spells hipster" in res:
                            res = "hipster"
                        if "c-l-i-c-k-e-r" in res:
                            res = "clicker"
                        if "c-o-n-c-e-p-t" in res:
                            res = "concept"
                        if res.strip().endswith("t o m o n e y a s t e r"):
                            res = "tomoneyaster"
                        if res.strip().endswith("p e r s o n a\n\nis that correct?"):
                            res = "persona"
                        if res.strip().endswith("correct corrinaopiningriguerenaultenduresclousertristar"):
                            res = "corrinaopiningriguerenaultenduresclousertristar"
                        if res.strip().endswith("romulus\n\nu n c o v e r"):
                            res = "uncover"
                        if res.strip().endswith("with no spaces or punctuation.\n\nretreat"):
                            res = "retreat"
                        if res.strip().endswith("insures\nlisabeth\nespinal\n\nmissiles"):
                            res = "missiles"
                        if res.strip().endswith("in the sequence \"audette uplinks conaway tristar infuses opining norwich\":\n\na u c t i o n"):
                            res = "auction"
                        if res.strip().endswith("overton pedealed topanga inscore madaras unimate marwood\n\noptimum"):
                            res = "optimum"
                        if "percent\n\nthis sequence" in res:
                            res = "percent"
                        if res.strip().endswith("combine the first letters of each word to form a new sequence.\n\ncreator"):
                            res = "creator"
                        if res.strip().endswith("risotto ourself midlife afirms noncash chugged excrete\n\nromance"):
                            res = "romance"
                        if res.strip().startswith("i am not able to provide an answer"):
                            res = ""
                        if res.strip().startswith("sunroom\ncrooper\nroister\namabile\ntrinkle\ncreason\nheight\n\n\n\nscratch"):
                            res = "scratch"
                        if res.strip().startswith("outmode folgers farwell excisis norvell stuarts espitia\n\noffense."):
                            res = "offense"
                        if res.strip().startswith("saviano caridad ardmore novelli narayan enson rockley\n\nscanner"):
                            res = "scanner"
                        if res.strip().startswith("ingalls norbeck stauber thumann archard norward thumann\n\ninstant."):
                            res = "instant"
                        if res.strip().startswith("i'm thinking of the answer being something like \"scanner\""):
                            res = "scanner"
                        if res.strip().startswith("the answer will be a sequence of letters, such as \"denmark\"."):
                            res = "denmark"
                        if len(res.strip()) > 8:
                            if res.strip()[7] == "\n" or (res.strip()[7] == "." and res.strip()[8] == "\n"):
                                words = res.strip().split()
                                if len(words) > 4:
                                    if words[1] == "the" and (words[2] == "letters" or words[2] == "first"):
                                        res = words[0]
                                    if words[1] == "this" and words[2] == "answer":
                                        res = words[0]
                                    if words[1] == "this" and words[2] == "is":
                                        res = words[0]
                                    if words[1] == "you" and words[2] == "combine":
                                        res = words[0]
                                

                        if "i have a question that's similar to this one. i need to know how to solve it. can you please help me?" in res:
                            print("RES")
                            print(res)
                            15/0
                        
                        res = res.replace(inp.lower(), "")
                        newline_inp = "\n".join(inp.split())
                        comma_inp = ", ".join(inp.split())
                        res = res.replace(newline_inp.lower(), "").replace(comma_inp.lower(), "")
                        
                        res = res.replace("\"", "")
                        res = res.replace(".", "")
                        res = res.replace("\n", " ")
                        res = res.replace(", ", " ")
                        res = res.replace(",", "")
                        res = res.replace("-", "")

                        res, first_three_single = join_single_letters(res)
                        if first_three_single:
                            # Conclude that the response starts with the answer, spelled out
                            res = res.split()[0]

                        for indicator_sequence in indicator_sequences:
                            if indicator_sequence in res:
                                truncated = res[res.index(indicator_sequence) + len(indicator_sequence):].strip()
                                res = truncated.split()[0]

                        words = res.split()
                        all_single = True
                        for word in words:
                            if len(word) != 1:
                                all_single = False
                        if all_single:
                            res = res.replace(" ", "")

                        res = res.replace("  ", " ")
                        words = res.split()
                        if len(words) >= 2:
                            if words[-2] == "is":
                                res = words[-1]
                            elif words[-1].startswith("is:"):
                                res = words[-1][3:]
                            elif "is:" in words:
                                next_word = words[words.index("is:") + 1]
                                if len(next_word) > 2:
                                    res = next_word
                            elif "are:" in words and words.index("are:") < len(words) - 1:
                                next_word = words[words.index("are:") + 1]
                                if len(next_word) > 2:
                                    res = next_word

                        words = res.split()
                        if len(words) > 1:
                            if words[1] == "explanation:":
                                res = words[0]





                        res = res.upper()
                        gt = gt.upper()

                        if res == "PRIMATE REDRESS IGNOBLE MANATEE ANNULAR TAUNTED ERASINGTHEREFORETHE ANSWER IS: PRIMATEGRESSIMATATETE":
                            res = "PRIMATEGRESSIMATATETE"

                        if res == "I + N + S + W + E + S + T = INSWEST":
                            res = "INSWEST"


                        # Checking if there are any answers that are not covered by the above cases
                        if res in manually_recognized_answers:
                            res = res.replace(" ", "")
                        elif gt not in res.replace(" ", ""):
                            # Don't need to worry in this case, because the correct answer is not in the response, so we can be confident that the model didn't produce the correct answer
                            pass
                        elif len(res.split()) != 1:
                            print(res)
                            print(temp_res)
                            print(inp)
                            print(words)
                            print("")
                            uncovered += 1
                            pass
    

                        dist = distance(gt, res)
                        total_dist += dist
                        dists.append(dist)

                        #if gt != res and gt in res:
                        #    print(gt)
                        #    print(res)
                        #    print("")

                        if gt == res:
                            count_correct += 1
                            correct = "1"
                            if model == "gpt-4-0613" and condition == "acronym1" and inner == 1 and outer == 1 and gt == "PARTIES":
                                #print(inp)
                                #print(gt)
                                #print(res)
                                #print("")
                                pass
                        else:
                            correct = "0"
                            if model == "gpt-4-0613" and condition == "acronym1" and inner == 1 and outer == 1 and gt == "PARTIES": # and len(gt) != len(res):
                                #print(inp)
                                #print(gt)
                                #print(res)
                                #print("")
                                pass
                        #    print(res, gt)
                        
                        if model == "gpt-4-0613" and condition == "acronym1" and inner == 5 and outer == 1 and gt != res:
                            #print(inp)
                            #print(gt)
                            #print(res)
                            #print("")
                            pass
                        count_total += 1

                        if model.startswith("gpt"):
                            data = [str(index), condition, saved_stats[inp]["n_characters"], saved_stats[inp]["n_gpt4_tokens"], saved_stats[inp]["gpt2_logprob"], 
                                    saved_stats[gt]["n_characters"], saved_stats[gt]["n_gpt4_tokens"], saved_stats[gt]["gpt2_logprob"], correct]
                        elif model == "llama-2-70b-chat":
                            data = [str(index), condition, saved_stats[inp]["n_characters"], llama_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                    saved_stats[gt]["n_characters"], llama_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                        elif model == "text-bison-001":
                            data = [str(index), condition, saved_stats[inp]["n_characters"], palm_tokens[inp], saved_stats[inp]["gpt2_logprob"],
                                    saved_stats[gt]["n_characters"], palm_tokens[gt], saved_stats[gt]["gpt2_logprob"], correct]
                        else:
                            14/0
                        fo.write("\t".join(data) + "\n")



                    print(condition + "_" + str(inner) + str(outer), "acc:", count_correct*1.0/count_total, "levdist:", total_dist*1.0/count_total, statistics.median(dists))

print(uncovered)
