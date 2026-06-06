def load_toy_data(args, split='test'):
    if args.data == 'csqa':
        questions = [
            "Where would a person usually keep a toothbrush?\n(A) refrigerator\n(B) bathroom\n(C) garage\n(D) mailbox\n(E) garden\n\n",
            "What do people commonly use to cut paper?\n(A) spoon\n(B) pillow\n(C) scissors\n(D) shoe\n(E) candle\n\n",
            "What is most likely needed to see in a dark room?\n(A) flashlight\n(B) blanket\n(C) fork\n(D) soap\n(E) notebook\n\n",
        ]
        labels = ["(B)", "(C)", "(A)"]
    elif args.data == 'formal_logic':
        questions = [
            "All mammals are warm-blooded. All whales are mammals. Which conclusion follows?\n(A) All whales are warm-blooded\n(B) No whales are mammals\n(C) Some mammals are not warm-blooded\n(D) All warm-blooded animals are whales\n\n",
            "If it rains, the ground gets wet. It is raining. What follows?\n(A) The ground gets wet\n(B) It is sunny\n(C) The ground stays dry\n(D) It did not rain\n\n",
            "No squares are circles. This shape is a square. Which statement is true?\n(A) This shape is a circle\n(B) This shape is not a circle\n(C) All circles are squares\n(D) No shapes exist\n\n",
        ]
        labels = ["(A)", "(A)", "(B)"]
    elif args.data == 'pro_medicine':
        questions = [
            "Which vitamin deficiency is classically associated with scurvy?\n(A) Vitamin A\n(B) Vitamin B12\n(C) Vitamin C\n(D) Vitamin D\n\n",
            "Which organ primarily pumps blood through the human body?\n(A) Liver\n(B) Heart\n(C) Kidney\n(D) Lung\n\n",
            "Which measurement is commonly used to assess fever?\n(A) Body temperature\n(B) Hair length\n(C) Shoe size\n(D) Eye color\n\n",
        ]
        labels = ["(C)", "(B)", "(A)"]
    elif args.data == 'hellaswag':
        questions = [
            "Can you choose the option that best follows:\n\"A chef cracks eggs into a bowl and heats a pan.\"\n(A) The chef starts painting a wall.\n(B) The chef cooks the eggs in the pan.\n(C) The chef mails a letter.\n(D) The chef turns off the kitchen lights and leaves immediately.\n\n",
            "Can you choose the option that best follows:\n\"A runner ties their shoes at the starting line.\"\n(A) The runner begins the race.\n(B) The runner bakes a cake.\n(C) The runner falls asleep in bed.\n(D) The runner writes a novel.\n\n",
            "Can you choose the option that best follows:\n\"A student opens a textbook before an exam.\"\n(A) The student reviews notes.\n(B) The student waters a tree.\n(C) The student repairs a car engine.\n(D) The student swims across a lake.\n\n",
        ]
        labels = ["(B)", "(A)", "(A)"]
    else:
        raise NotImplementedError(f"No toy dataset is defined for {args.data}")

    size = args.data_size or len(questions)
    return questions[:size], labels[:size]
