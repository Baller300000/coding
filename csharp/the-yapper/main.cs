namespace System;

class Magic8Ball
{
    private static readonly List<string> philosophy = new()
    {
       "The only true wisdom is in knowing you know nothing. - Socrates\n",
        "I think, therefore I am. - René Descartes\n",
        "The unexamined life is not worth living. - Socrates\n",
        "Happiness is not something ready made. It comes from your own actions. - Dalai Lama\n",
        "The only way to do great work is to love what you do. - Steve Jobs\n",
        "In the middle of difficulty lies opportunity. - Albert Einstein\n",
        "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela\n",
        "Life is what happens when you're busy making other plans. - John Lennon\n",
        "The best way to predict the future is to invent it. - Alan Kay\n",
        "Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson\n",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt\n",
        "The mind is everything. What you think you become. - Buddha\n",
        "The only thing I know is that I know nothing. - Socrates\n",
        "The greatest wealth is to live content with little. - Plato\n",
        "SAY MY NAME - Walter White\n",
        "You're goddman right - Walter White\n",
        "You like kissing bois dont you? You fucking furry weirdo - Boykisser :3\n",
    };
    private static readonly List<string> dadjokes = new()
    {
       "Why don't scientists trust atoms? Because they make up everything!\n",
        "Why did the scarecrow win an award? Because he was outstanding in his field!\n",
        "Why don't skeletons fight each other? They don't have the guts!\n",
        "What do you call fake spaghetti? An impasta!\n",
        "Why did the bicycle fall over? Because it was two-tired!\n",
        "What do you call cheese that isn't yours? Nacho cheese!\n",
        "Why did the tomato turn red? Because it saw the salad dressing!\n",
        "What do you call a bear with no teeth? A gummy bear!\n",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!\n",
        "What do you call a snowman with a six-pack? An abdominal snowman!\n",
        "Why did the math book look sad? Because it had too many problems!\n",
        "What do you call a fish that wears a crown? A king fish!\n",
        "Why did the chicken go to the seance? To talk to the other side!\n",
        "What do you call a dog that can do magic? A labracadabrador!\n",
        "Why did the coffee file a police report? It got mugged!\n",
    };
    private static readonly List<string> eviljokes = new()
    {
        "Where did little Timmy go after getting lost in a minefield? Everywhere.\n",
        "What's the difference between a snowman and a snowwoman? Snowballs.\n",
        "What did the cannibal get when he was late for dinner? The cold shoulder.\n",
        "What did the Nazi say when he was asked to stop? 'I can't stop, I'm on a roll!'\n",
        "Nock nock\nWho's there?\nVE VILL ASK ZE KVUESTIONZ\n",
        "Why did 9/11 happen? Because the Twin Towers were too tall and needed to be brought down.\n",
        "What do you call a man with no arms and no legs in a pool? Bob.\n"
    };
    static void Main()
    {
        Random random = new();

        Console.WriteLine("╔══════════════════════════════════╗");
        Console.WriteLine("║            THE YAPPER            ║");
        Console.WriteLine("╚══════════════════════════════════╝");
        Console.WriteLine();

        while (true)
        {
            Console.Write("I am The Yapper and I will talk to you about random shit\n");
            Console.Write("Let's talk (/help for more info): ");
            string? input = Console.ReadLine();

            if (input.Equals("/help", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nCommand list:");
                Console.WriteLine("/help - Show this help message\n");
                Console.WriteLine("/quit - Exit the program\n");
                Console.WriteLine("/philosophy - Spew out bullshit philosophy\n");
                Console.WriteLine("/saymyname - SAY MY NAME\n");
                Console.WriteLine("/jokes dad - get a dad joke\n");
                Console.WriteLine("/jokes evil - get an evil joke\n");
                Console.WriteLine("just talk to me for anything\n");
                continue;
            }
            if (input.Equals("/quit", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nAight bye");
                break;
            }
            if (input.Equals("/saymyname", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nWalt: You all know exactly who I am. Say my name.\nDeclan: Do it? I don't have a damn clue who the hell you are.\nWalt: Yeah, you do. I'm the cook. I'm the man who killed Gus Fring.\nDeclan: [pauses] Heisenberg.\nWalt: You're goddamn right.\n");
                continue;
            }
            if (input.Equals("/philosophy", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n" + philosophy[random.Next(0, philosophy.Count)] + "\n");
                continue;
            }
            if (input.Equals("/jokes dad", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n" + dadjokes[random.Next(0, dadjokes.Count)] + "\n");
                continue;
            }
            if (input.Equals("/jokes evil", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n" + eviljokes[random.Next(0, eviljokes.Count)] + "\n");
                continue;
            }
            if (input.Equals("/jokes", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nHavent made that yet\n");
            }
            // --------------------
            // this is a joke, dont take seriously!!!
            if (input.Equals("seig", StringComparison.OrdinalIgnoreCase)
            || input.Equals("heil", StringComparison.OrdinalIgnoreCase)
            || input.Equals("SEIG", StringComparison.OrdinalIgnoreCase)
            || input.Equals("HEIL", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nHEIL! (joking ofc)\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            if (input.Equals("is it gay to like femboys?", StringComparison.OrdinalIgnoreCase)
            || input.Equals("is it gay to like femboys", StringComparison.OrdinalIgnoreCase)
            || input.Equals("Is it gay to like femboys", StringComparison.OrdinalIgnoreCase)
            || input.Equals("Is it gay to like femboys?", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nU like them bc they look like women, then no, \nbut if u like theb bc of their personality then yes, mr weirdo\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            if (input.Equals("\ndeus vult", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDEUS VULT", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDeus Vult", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\ndeus vult!", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDEUS VULT!", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDeus Vult!", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n DEUS VULT\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            // --------------------
            if (input.IsWhiteSpace() || string.IsNullOrEmpty(input))
            {
                Console.WriteLine("\nSAY MY NAME");
                continue;
            }

            Console.WriteLine("\nTHE IDIOT IS THINKING...");
            Console.WriteLine();
        }
    }
}
