"""
Pet Care Knowledge Base
Contains veterinary guidelines and health recommendations sourced from:
- ASPCA (aspca.org) - Dog and Cat Nutrition Tips, General Cat Care
- VCA Animal Hospitals (vcahospitals.com) - Healthy Exercise for Dogs
- American Humane (americanhumane.org) - Exercising Your Pet
- Colorado State University CHHS (chhs.source.colostate.edu) - Exercise Good for You and Your Pet
- Hill's Pet (hillspet.com) - Exercise and Game Ideas for Dogs
- Dr. Peter Dobias (peterdobias.com) - Common Mistakes When Exercising Dogs
- WebMD Pets (webmd.com) - How to Exercise With Your Dog
- Oakland Veterinary Referral Services (ovrs.com) - Small Daily Habits for Pet Health
- ASPCA (aspca.org) - General Dog Care
- Gardens Animal Hospital (gardensanimalhospital.com) - Preventative Pet Care Guide
- Bhatt Vet Specialty (bhattvetspecialty.com) - Daily Pet Care Tips
- Mission Veterinary Specialists (missionveterinaryspecialists.com) - Healthy Pet Checklist
- Mokena Animal Clinic (mokenaanimalclinic.com) - Pet Care Tips at Home
- NaturVet (naturvet.com) - 5 Health Tips for Basic Pet Care
- Family Pet Care Vets (fpcvets.com) - The Ultimate Pet Wellness Routine
- Mental Health America (mhanational.org) - Understanding Your Pet's Needs
- Vetster (vetster.com) - How to Exercise With Your Cat
- Tractive (tractive.com) - How Much Exercise Does a Cat Need
- AVMA (avma.org) - Caring for Senior Cats and Dogs
- VCA Animal Hospitals (vcahospitals.com) - Senior Dog Care
- RSPCA (rspca.org.uk) - Caring for Older Dogs
- AKC (akc.org) - Puppy Socialization
- Texas A&M VMBS (vetmed.tamu.edu) - Puppy Socialization Guide
- AAHA (aaha.org) - Enrichment for Pet Mental and Emotional Wellbeing
- Ocean Animal Hospital (oceananimalhospital.com) - Importance of Pet Enrichment
- Cornell Feline Health Center (vet.cornell.edu) - Cat Hydration
- Woofie's (woofies.com) - How Often to Groom Your Dog
- Newport Veterinary (newportvetrh.com) - Dog Grooming Frequency Guide
- Haw Creek Animal Hospital (hawcreekanimalhospital.com) - Senior Cat Nutrition
- PetMD (petmd.com) - Senior Cat Nutrition and Health
"""

# Pet care documents indexed as a knowledge base
PET_CARE_DOCUMENTS = [
    {
        "id": "dog_feeding",
        "title": "Dog Feeding Guidelines",
        "source": "ASPCA - aspca.org/pet-care/dog-care/dog-nutrition-tips",
        "content": """
        Source: ASPCA (aspca.org/pet-care/dog-care/dog-nutrition-tips)
        All dogs should be fed twice daily, with meals spaced 8 to 12 hours apart.
        Divide the total daily recommended amount into two equal meals.
        Puppies require twice the energy intake of adult dogs and need food
        containing 25-30% protein. Small breed puppies can be fed free-choice,
        but medium, large, and giant breeds need controlled portions to prevent
        bone and joint problems.
        Senior diet by breed size:
          - Small breeds (under 20 lbs): begin senior diet at 7 years
          - Medium breeds (21-50 lbs): begin senior diet at 7 years
          - Large breeds (51-90 lbs): begin senior diet at 6 years
          - Giant breeds (91+ lbs): begin senior diet at 5 years
        Treats should represent 5% or less of the dog's daily food intake.
        Always provide fresh water. Feeding time per meal: 5-10 minutes.
        """
    },
    {
        "id": "dog_exercise",
        "title": "Dog Exercise Requirements",
        "source": "VCA Animal Hospitals - vcahospitals.com/know-your-pet/healthy-exercise-for-dogs | American Humane - americanhumane.org/public-education/exercising-your-pet | CSU CHHS - chhs.source.colostate.edu/exercise-good-for-you-and-your-pet",
        "content": """
        Sources: VCA Animal Hospitals (vcahospitals.com), American Humane (americanhumane.org),
        Colorado State University CHHS (chhs.source.colostate.edu)

        Daily exercise by energy level (American Humane):
          - High energy breeds: 60 to 90 minutes of activity daily
          - Moderate energy breeds: 30 to 60 minutes daily
          - Senior dogs: several short walks or gentle play sessions daily

        Daily walking routine (CSU CHHS): 20-30 minutes a day is recommended.
        Consistency matters (VCA): it is better to take a 20-minute walk every day
        than a 2-hour walk once a week.

        Puppies (VCA): avoid lengthy running sessions; offer short spurts of play
        where they can set their own pace. Leashed walks are fine but shouldn't be excessive.
        Introduce exercise slowly to protect growing joints.

        Senior/health-compromised dogs (VCA): requires veterinary evaluation before
        starting any exercise program.

        Breed-specific notes (VCA):
          - Brachycephalic breeds (pugs, bulldogs, Pekingese): need specialized
            cardiovascular programs and have difficulty cooling down.
          - Overweight/obese dogs: poor candidates for sudden start/stop activities
            like ball chasing; begin with slow progressive walking.

        Exercise types (American Humane): neighborhood walks, fetch, trail hikes,
        agility play, puzzle feeders, treat hunts, playtime with other dogs.
        Swimming is also beneficial — introduce gradually as not all dogs enjoy water (VCA).

        Hot weather: exercise only during cooler hours (early morning or evening).
        Always consult a vet before starting a new exercise program (VCA, CSU CHHS).
        """
    },
    {
        "id": "dog_grooming",
        "title": "Dog Grooming Schedule",
        "source": "ASPCA - aspca.org/pet-care/dog-care/grooming-your-dog",
        "content": """
        Source: ASPCA (aspca.org/pet-care/dog-care/grooming-your-dog)
        Brushing: daily for long-haired breeds, 2-3 times weekly for short-haired breeds.
        Brushing duration: 10-20 minutes per session depending on coat length.
        Bathing: every 4-12 weeks depending on breed and activity level.
        Bath time: 15-30 minutes including drying.
        Nail trimming: every 4-8 weeks, takes 5-10 minutes.
        Ear cleaning: weekly for floppy-eared breeds, approximately 5 minutes.
        Dental care: daily brushing recommended, takes 2-5 minutes.
        Professional grooming: every 6-8 weeks for double-coated breeds,
        every 8-12 weeks for others.
        """
    },
    {
        "id": "cat_feeding",
        "title": "Cat Feeding Guidelines",
        "source": "ASPCA - aspca.org/pet-care/cat-care/cat-nutrition-tips",
        "content": """
        Source: ASPCA (aspca.org/pet-care/cat-care/cat-nutrition-tips)
        All cats should be fed twice daily using portion control, meals spaced 8-12 hours apart.
        Kittens require 2-3 times the energy of adult cats and about 30% of energy from protein.
        Kittens can be fed free-choice (food available at all times) until maturity around one year.
        Kitten feeding stages:
          - Newborn to 4 weeks: mother's milk only
          - 4-6 weeks: begin weaning; introduce kitten food while nursing
          - 5-10 weeks: transition fully to solid kitten food
        Senior cats (7+ years): start on a senior diet at about seven years of age.
        Treats should represent 5% or less of a cat's daily food intake.
        Fresh water must always be available.
        Taurine (found only in animal-based proteins) is essential for all cats.
        Feeding time per meal: approximately 5 minutes.
        """
    },
    {
        "id": "cat_play",
        "title": "Cat Play and Enrichment",
        "source": "American Humane - americanhumane.org/public-education/exercising-your-pet | ASPCA - aspca.org/pet-care/cat-care/general-cat-care | CSU CHHS - chhs.source.colostate.edu/exercise-good-for-you-and-your-pet",
        "content": """
        Sources: American Humane (americanhumane.org), ASPCA (aspca.org),
        Colorado State University CHHS (chhs.source.colostate.edu)

        Cats need two or more play sessions each day (American Humane).
        Each session can last 10 to 15 minutes (American Humane).
        Ten minutes may be enough for cats in a single session (CSU CHHS).

        Activity types (American Humane):
          - Interactive wand toys that mimic prey movement
          - Laser pointer play — always end with a physical toy the cat can "catch"
            to complete the hunting cycle
          - Vertical climbing spaces (cat trees, wall shelves)
          - Treat hunts or puzzle feeders
          - Hunt-and-play sessions two or three times daily

        Additional enrichment (ASPCA):
          - Scratching post at least 3 feet high (sisal, burlap, or bark)
          - Window perches for passive enrichment
          - Indoor cats need more enrichment than outdoor cats

        Senior or health-compromised cats: gentle, low-impact play; consult a vet
        before starting new routines (American Humane).
        """
    },
    {
        "id": "cat_grooming",
        "title": "Cat Grooming and Hygiene",
        "source": "ASPCA - aspca.org/pet-care/cat-care/general-cat-care",
        "content": """
        Source: ASPCA (aspca.org/pet-care/cat-care/general-cat-care)
        Most cats groom themselves but benefit from regular supplemental grooming.
        Frequent brushing keeps the coat clean, reduces shedding, and reduces hairballs.
        Brushing: long-haired cats 5-7 times weekly; short-haired cats 2-3 times weekly.
        Brushing time: 5-10 minutes per session.
        Bathing: rarely needed unless cat gets dirty; 15-20 minutes including drying.
        Nail trimming: every 2-3 weeks keeps nails relatively blunt (ASPCA).
        Ear cleaning: monthly check and cleaning if needed, approximately 5 minutes.
        Dental care: daily brushing recommended, takes 2-3 minutes.
        Litter box: scoop solid waste at least once daily.
        Full litter change and box wash: at least weekly (less often with clumping litter).
        Daily litter maintenance: 5-10 minutes.
        """
    },
    {
        "id": "health_checkups",
        "title": "Veterinary Checkup Schedule",
        "source": "ASPCA - aspca.org | VCA Animal Hospitals - vcahospitals.com",
        "content": """
        Sources: ASPCA (aspca.org), VCA Animal Hospitals (vcahospitals.com)
        Regular veterinary care is essential for pet health.
        Always consult a veterinarian before starting any new exercise or diet program,
        especially for senior, overweight, or health-compromised pets (VCA).
        Kittens: spaying/neutering recommended by five months of age (ASPCA).
        Adult pets (1-7 years): annual checkup and vaccinations minimum.
        Senior pets (7+ years): every 6 months is recommended.
        Each checkup: 30-60 minutes depending on clinic and procedures.
        Vaccinations: follow vet's recommended schedule (typically yearly or tri-annually).
        Dental cleaning: professional cleaning every 1-3 years, takes 1-2 hours at clinic.
        Parasite prevention: monthly to quarterly depending on prevention method.
        Screen dogs for cardiac, pulmonary, pain, hypothyroidism, and heart disease
        before beginning any exercise program (VCA).
        """
    },
    {
        "id": "training",
        "title": "Pet Training and Socialization",
        "source": "ASPCA - aspca.org | American Humane - americanhumane.org",
        "content": """
        Sources: ASPCA (aspca.org), American Humane (americanhumane.org)
        Training is important for safety and behavior management.
        Puppies (8-16 weeks): puppy kindergarten classes; 10-15 min daily practice at home.
        Dogs: ongoing training and practice 10-30 minutes daily for best results.
        Obedience training: professional classes typically 1 hour weekly.
        Socialization: puppies need gradual exposure to people, places, and sounds
        in 15-30 minute sessions.
        Puzzle feeders and treat hunts also provide mental stimulation alongside training.
        Cats: can benefit from clicker training and enrichment, 5-10 minutes daily.
        Behavior problems need dedicated training time of 15-30 minutes daily.
        """
    },
    {
        "id": "special_needs",
        "title": "Special Care and Exercise Safety",
        "source": "VCA Animal Hospitals - vcahospitals.com | American Humane - americanhumane.org | CSU CHHS - chhs.source.colostate.edu",
        "content": """
        Sources: VCA Animal Hospitals (vcahospitals.com), American Humane (americanhumane.org),
        Colorado State University CHHS (chhs.source.colostate.edu)

        General safety: always consult a vet before starting new exercise routines,
        especially for pets with existing health conditions (VCA, American Humane, CSU CHHS).
        Begin any new program gradually and build slowly (American Humane, VCA).

        Overweight/obese dogs (VCA): poor candidates for sudden start/stop activities;
        begin with slow progressive walking. Over half of U.S. dogs and cats are
        overweight or obese (American Humane).

        Brachycephalic breeds (pugs, bulldogs): have difficulty cooling; need specialized
        low-intensity cardiovascular programs (VCA).

        Hot weather (VCA, ASPCA): exercise only during cooler hours — early morning
        or end of day — to prevent heatstroke.

        Senior pets (American Humane): benefit from gentle activities such as slow walks
        or light play; avoid high-impact or high-intensity exercise.

        Arthritic pets: warm-up exercise and pain management recommended (10-15 minutes).
        Diabetic pets: insulin administration and blood glucose monitoring (5-10 minutes).
        Injured/recovering pets: follow vet guidance strictly; limited activity only.
        """
    },
    {
        "id": "dog_feeding_stages",
        "title": "Dog Feeding Schedule by Life Stage",
        "source": "ASPCA - aspca.org/pet-care/dog-care/general-dog-care",
        "content": """
        Source: ASPCA (aspca.org/pet-care/dog-care/general-dog-care)

        Puppy feeding schedule by age:
          - 8 to 12 weeks: four meals daily
          - 3 to 6 months: three meals daily
          - 6 months to 1 year: two meals daily
          - Adult dogs (1+ year): one meal daily; larger breeds or those prone to
            bloat benefit from two smaller meals instead

        Premium-quality dry food provides a well-balanced diet for adult dogs and
        can be mixed with water, broth, or a small amount of canned food.
        Human foods should comprise no more than 10% of daily intake.
        Spaying or neutering should be completed by six months of age.
        Provide a warm, quiet place to rest away from drafts with proper bedding.
        Always include ID tags, collar licensing, and microchipping for safety.
        """
    },
    {
        "id": "pet_dental_care",
        "title": "Pet Dental Care Guidelines",
        "source": "NaturVet - naturvet.com | Gardens Animal Hospital - gardensanimalhospital.com | Oakland Veterinary Referral Services - ovrs.com | Mission Veterinary Specialists - missionveterinaryspecialists.com",
        "content": """
        Sources: NaturVet (naturvet.com), Gardens Animal Hospital (gardensanimalhospital.com),
        Oakland Veterinary Referral Services (ovrs.com),
        Mission Veterinary Specialists (missionveterinaryspecialists.com)

        Most pets show signs of dental disease by age three (Gardens Animal Hospital).
        57% of dogs and 60% of cats in America are overweight or obese (NaturVet).

        Brushing frequency:
          - Ideal: daily brushing with pet-safe toothpaste (ASPCA, Gardens Animal Hospital)
          - Minimum: 2-3 times per week (NaturVet)
          - Duration: 2-5 minutes per session

        How to introduce brushing (NaturVet):
          - Start with toothpaste on a finger
          - Gradually increase coverage over time
          - Always use pet-formulated toothpaste — never human toothpaste

        Dental alternatives when brushing is not possible:
          - Dental chews verified by the Veterinary Oral Health Council (NaturVet)
          - Oral water additives (OVRS, Bhatt Vet)
          - Dental diets as recommended by a veterinarian

        Professional dental cleanings: schedule as recommended by your vet,
        typically every 1-3 years (ASPCA).
        Weekly: provide dental chew or brush teeth (Mission Vet checklist).
        """
    },
    {
        "id": "pet_daily_weekly_routine",
        "title": "Pet Daily, Weekly, and Monthly Care Routine",
        "source": "Mission Veterinary Specialists - missionveterinaryspecialists.com | Oakland Veterinary Referral Services - ovrs.com | Bhatt Vet Specialty - bhattvetspecialty.com | Mokena Animal Clinic - mokenaanimalclinic.com",
        "content": """
        Sources: Mission Veterinary Specialists (missionveterinaryspecialists.com),
        Oakland Veterinary Referral Services (ovrs.com),
        Bhatt Vet Specialty (bhattvetspecialty.com),
        Mokena Animal Clinic (mokenaanimalclinic.com)

        DAILY tasks:
          - Provide fresh, clean water at all times (Mission Vet, OVRS)
          - Feed a nutritionally balanced diet appropriate for age, size, and breed
          - Exercise: brisk walks, interactive play, or agility training
            (example: 30-minute walk 2-3 times a day — Bhatt Vet)
          - Short walks — even two or three brief walks per day help (OVRS)
          - At least a few minutes of enrichment: puzzle feeders, sniff games,
            training practice (OVRS)
          - Check coat for matting, lumps, bumps, scabs, and parasites (OVRS)
          - Monitor for changes in appetite, energy, or behavior (Bhatt Vet)
          - Maintain consistent schedule for meals, exercise, and bedtime (OVRS)

        WEEKLY tasks:
          - Inspect ears for redness, odor, or excess wax (Mission Vet)
          - Examine skin and coat for lumps, bumps, or parasites (Mission Vet)
          - Brush teeth or provide dental chew (Mission Vet)
          - Clean and rotate toys (Mission Vet)
          - Daily brushing for long-haired pets (Mission Vet)

        MONTHLY tasks:
          - Administer flea, tick, and heartworm preventatives as recommended (Mission Vet)
          - Monitor pet weight (Mission Vet)
          - Deep clean litter box and disinfect (cats — Mission Vet)
          - Bathe based on breed and lifestyle (Mission Vet)
          - Wash paws after outdoor activity to remove pesticides, antifreeze, salt (Bhatt Vet)

        YEARLY tasks:
          - Annual or biannual veterinary wellness exam (Mission Vet, Gardens Animal Hospital)
          - Professional dental cleaning when recommended
          - Update microchip and ID tag information
          - Routine blood work, especially for senior pets (Mission Vet)

        Grooming safety note (Mokena): matted, dirty coats can trap heat and debris,
        risking skin irritation and infection. Long claws can cause injury.
        """
    },
    {
        "id": "pet_weight_nutrition",
        "title": "Pet Weight Management and Nutrition",
        "source": "NaturVet - naturvet.com | Gardens Animal Hospital - gardensanimalhospital.com | Oakland Veterinary Referral Services - ovrs.com",
        "content": """
        Sources: NaturVet (naturvet.com), Gardens Animal Hospital (gardensanimalhospital.com),
        Oakland Veterinary Referral Services (ovrs.com)

        Weight check (NaturVet): a healthy pet should have a gentle inward dip from
        the last rib to the hips when viewed from above, and an upward belly slope
        from rib to groin when viewed from the side.

        Obesity statistics: 57% of dogs and 60% of cats in America are overweight
        or obese (NaturVet). Regular daily exercise is critical for prevention.

        Treat allowance:
          - NaturVet: no more than 5-10% of daily diet
          - ASPCA: treats at 5% or less of daily intake
          - Avoid table scraps and excessive human food (Gardens Animal Hospital, OVRS)

        Nutrition guidelines:
          - Select high-quality food appropriate for age and activity level
          - Choose diets with meat as a top ingredient (NaturVet)
          - Look for AAFCO statement on packaging to verify nutritional completeness
          - Rotate protein sources and consider adding fresh fruits/vegetables
          - Home-cooked diets: consult a veterinary nutritionist, especially for cats
            (true carnivores requiring specific nutrients like taurine)
          - Measure portions to maintain healthy body weight (OVRS)
          - Consider wet food or water fountains if pet drinks insufficiently (OVRS)

        Supplements: choose products bearing the National Animal Supplement Council
        seal and consult a veterinarian before adding any supplement (NaturVet).
        """
    },
    {
        "id": "pet_wellness_routine",
        "title": "Complete Pet Wellness Routine",
        "source": "Family Pet Care Vets - fpcvets.com/the-ultimate-pet-wellness-routine | Mental Health America - mhanational.org/resources/understanding-your-pets-needs",
        "content": """
        Sources: Family Pet Care Vets (fpcvets.com),
        Mental Health America (mhanational.org)

        Daily wellness routine by time of day (Family Pet Care Vets):
          Morning:
            - Dogs: walk, fetch, agility games, or tug-of-war
            - Cats: laser pointer, climbing tower, or wand toy session
            - Small animals: playpen time or rotated enrichment toys
            - Serve high-quality, vet-approved breakfast suited to age and health needs
          Midday:
            - Interactive toys: puzzle feeders, treat-dispensing balls, sniff mats
            - Sensory enrichment: window access, nature sounds, or new scents
            - Pet cameras or interactive feeders if owner is away
          Evening:
            - Balanced dinner with appetite monitoring
            - Coat brushing, nail checks, ear cleaning, inspection for fleas or bumps
            - Brush teeth daily to prevent costly future dental treatments
            - Wash food and water bowls daily to prevent bacteria buildup
            - Quiet rest period in a calm, comfortable space

        Fresh, clean water must always be available; consider water fountains.
        Daily exercise reduces destructive behavior, anxiety, and obesity (FPC Vets).
        Consistent daily schedules for meals, walks, and play support emotional well-being.

        Monthly wellness tasks (Family Pet Care Vets):
          - Flea and tick prevention
          - Heartworm medication
          - Nail trims
          - Weight monitoring

        Mental health and bonding (Mental Health America):
          - Frequent positive interactions strengthen the human-animal bond
          - Activities like feeding, walking, and playing provide routine and purpose
          - Include pets in daily life through varied experiences for mental stimulation
          - Cats often hide pain — preventative vet care is especially important for cats

        Training (Mental Health America):
          - Positive reinforcement training prevents unwanted behavior
          - Builds trust and communication between pet and owner
          - Establishes the foundation of a healthy, lasting human-animal bond

        Veterinary visits (Mental Health America):
          - Healthy adult dogs: annual check-ups minimum
          - Older dogs: more frequent visits as needed
          - Always consult a vet for behavioral concerns, exercise needs, or weight questions
        """
    },
    {
        "id": "cat_exercise",
        "title": "Cat Exercise Guidelines",
        "source": "Vetster - vetster.com | Tractive - tractive.com | Clyde's Animal Clinic - clydesanimalclinic.com",
        "content": """
        Sources: Vetster (vetster.com), Tractive (tractive.com), Clyde's Animal Clinic (clydesanimalclinic.com)

        Regular exercise is important for cats' heart, lungs, muscles, and joint health (Vetster).
        Exercise keeps cats at a healthy weight, provides mental enrichment, and strengthens
        the bond between cat and owner (Vetster).

        Activity ideas for cats:
          - Laser pointers and feather wands for interactive play
          - Cardboard box mazes for exploration
          - Solo play options like tunnels and battery-operated toys for when owners are busy
          - Building agility courses or exploring new environments

        A veterinarian can provide a personalized recommendation based on the cat's
        condition and health status (Tractive).
        Combine play with a balanced diet, portion control, and routine veterinary check-ups.
        Indoor cats especially need regular daily exercise to prevent obesity and boredom.
        """
    },
    {
        "id": "senior_pet_care",
        "title": "Senior Pet Care Guidelines",
        "source": "AVMA - avma.org | VCA Animal Hospitals - vcahospitals.com | RSPCA - rspca.org.uk | Haw Creek Animal Hospital - hawcreekanimalhospital.com | PetMD - petmd.com",
        "content": """
        Sources: AVMA (avma.org), VCA Animal Hospitals (vcahospitals.com),
        RSPCA (rspca.org.uk), Haw Creek Animal Hospital (hawcreekanimalhospital.com),
        PetMD (petmd.com)

        Age is not a disease — senior pets need extra care and attention but can still
        live full, healthy lives with proper management (AVMA).

        Senior dog care (AVMA, VCA, RSPCA):
          - Vet exams every 6 months, including dental care, bloodwork, and checks for
            aging-related diseases like arthritis and heart disease
          - Brush frequently to prevent mats — mats contribute to skin infections (VCA)
          - Older dogs may have reduced hearing/eyesight — avoid sudden loud noises (RSPCA)
          - Report behavior changes to a vet — they may signal underlying health issues (RSPCA)
          - Chest and abdominal X-rays may be recommended to screen for disease (VCA)
          - Diet: senior pets often need more easily digested food with adjusted nutrients (AVMA)

        Senior cat care (Haw Creek, PetMD):
          - Nutrition is the foundation of senior cat care — feed high-quality protein,
            healthy fats, and fiber to prevent age-related conditions
          - Senior cats (7+) may need to drink more water than younger cats to protect
            kidney function — consider water fountains or hydration supplements (PetMD)
          - Puzzle feeders and indoor hunting kits placed in easy-to-reach locations
            help keep senior cats cognitively sharp (PetMD)
          - Avoid foods that are hard to digest or high in phosphorus (kidney risk)
        """
    },
    {
        "id": "puppy_socialization",
        "title": "Puppy Socialization and Training Schedule",
        "source": "AKC - akc.org | Texas A&M VMBS - vetmed.tamu.edu | VCA Animal Hospitals - vcahospitals.com",
        "content": """
        Sources: AKC (akc.org), Texas A&M VMBS (vetmed.tamu.edu),
        VCA Animal Hospitals (vcahospitals.com)

        Socialization is just as important for puppies' emotional health as physical care (Texas A&M).
        Well-socialized puppies grow into well-adjusted adult dogs.

        Puppy training schedule by age (VCA):
          - 8–12 weeks: prime socialization window; introduce new people, sounds,
            environments in short positive sessions (15–20 min)
          - 12–16 weeks: puppy kindergarten classes recommended (AKC)
          - After 6 weeks of class: puppies can earn AKC S.T.A.R. Puppy title by passing
            a basic skills test (petting tolerance, sitting, basic commands)

        Warning signs to watch (Texas A&M):
          - Aggression over food or objects
          - Fear of new stimuli
          Puppies left with these behaviors often grow into aggressive or fearful adults —
          address early with professional training.

        Daily training sessions: 10–15 minutes, short and positive.
        Socialization sessions: 15–30 minutes, gradual exposure to new stimuli.
        Puppy classes: typically 1 hour weekly for 6 weeks.
        """
    },
    {
        "id": "pet_enrichment_mental_health",
        "title": "Pet Mental Health and Enrichment",
        "source": "AAHA - aaha.org | Ocean Animal Hospital - oceananimalhospital.com | San Bernardino Animal Care - animalcare.sbcounty.gov",
        "content": """
        Sources: AAHA (aaha.org), Ocean Animal Hospital (oceananimalhospital.com),
        San Bernardino County Animal Care (animalcare.sbcounty.gov)

        Enrichment refers to activities, toys, or environments designed to stimulate a
        pet's physical, mental, and emotional well-being (San Bernardino Animal Care).
        Studies show daily enrichment reduces stress, aids infection prevention, and
        significantly improves mental and physical health (San Bernardino Animal Care).

        Types of enrichment (AAHA):
          - Physical: movement and activity to prevent excess energy turning into
            destructive behavior
          - Social: interaction with people and other animals builds trust and confidence
          - Cognitive: puzzle feeders, training games, scent work

        For dogs (AAHA):
          - Balanced physical outlets help prevent destructive behavior
          - Social enrichment fulfills the need for connection and companionship

        For cats (AAHA):
          - Appropriate play reduces unwanted scratching and nighttime activity
          - Cats benefit from consistent, respectful interaction
          - Predictability builds trust and reduces anxiety

        Enrichment is not a luxury — it is an essential part of overall pet care (Ocean Animal Hospital).
        Activities should be tailored to each individual pet's species, age, and personality.
        """
    },
    {
        "id": "cat_hydration",
        "title": "Cat Hydration and Water Intake",
        "source": "Cornell Feline Health Center - vet.cornell.edu | Stella & Chewy's - stellaandchewys.com | Food Fur Life - foodfurlife.com",
        "content": """
        Sources: Cornell Feline Health Center (vet.cornell.edu),
        Stella & Chewy's (stellaandchewys.com), Food Fur Life (foodfurlife.com)

        Maintaining proper hydration is essential for cats' temperature regulation,
        digestion, and organ function (Cornell Feline Health Center).

        Daily water needs: cats need 8–27 tablespoons of water per day depending on
        environment, health status, and activity level (Food Fur Life).

        Wild cats obtain most moisture from prey — domesticated cats provided only
        a water bowl may not drink enough (Stella & Chewy's).

        Dehydration check (Cornell): gently pinch the skin at the back of the neck.
        In a hydrated cat it snaps back immediately; in a dehydrated cat it stays
        "tented." Geriatric cats are especially prone to dehydration.

        Urinary problems in cats are commonly a result of dehydration — dehydration
        can lead to urinary tract infections and blockages (Stella & Chewy's).

        Tips to increase water intake:
          - Use a cat water fountain (moving water encourages drinking)
          - Place multiple water stations around the home
          - Feed wet food to supplement hydration
          - Use bowls that monitor and auto-refill water intake
          - Senior cats (7+) especially need more water to protect kidney function (PetMD)
        """
    },
    {
        "id": "dog_grooming_by_breed",
        "title": "Dog Grooming Frequency by Coat Type",
        "source": "Woofie's - woofies.com | Newport Veterinary - newportvetrh.com | Backyard Pet Services - backyardpetservices.com",
        "content": """
        Sources: Woofie's (woofies.com), Newport Veterinary (newportvetrh.com),
        Backyard Pet Services (backyardpetservices.com)

        Grooming is a vital part of a dog's overall wellness — it prevents painful mats,
        skin infections, and other health issues (Woofie's).
        Regular grooming also helps identify skin irritation, fleas, ticks, and lumps early (Newport Vet).

        Grooming frequency by coat type (Woofie's, Backyard Pet Services):
          - Short/Smooth coats (Beagles, Boxers, Greyhounds): low maintenance, brush
            weekly to remove loose fur; bathe every 6–8 weeks
          - Double coats (Golden Retrievers, Huskies, German Shepherds): dense undercoat
            requires brushing 3–4 times weekly; bathe every 4–6 weeks; heavy seasonal shedding
          - Long coats: daily brushing required to prevent tangling and matting;
            professional grooming every 6–8 weeks
          - Curly/Wavy coats (Poodles, Doodles): brush every 1–2 days to prevent matting;
            professional grooming every 6–8 weeks

        Benefits of regular brushing (Newport Vet):
          - Removes loose fur and prevents mats
          - Distributes skin oils, keeping coat shiny and skin healthy
          - Prevents dirt and debris buildup

        Each breed has unique coat needs — understanding your dog's coat type determines
        the ideal brushing, bathing, and trimming schedule (Backyard Pet Services).
        """
    },
    {
        "id": "dog_exercise_games",
        "title": "Dog Exercise Games and Activity Ideas",
        "source": "Hill's Pet - hillspet.com/dog-care/play-exercise/exercise-and-game-ideas-for-dogs | WebMD Pets - webmd.com/pets/dogs/how-to-exercise-with-your-dog",
        "content": """
        Sources: Hill's Pet (hillspet.com), WebMD Pets (webmd.com)

        Recommended exercise activities (Hill's Pet):
          - Power walks with intervals: mix jogging, running, or high stepping during walks
          - Resistance walks on varied surfaces (sand, water, leaves, snow, rough terrain)
            to build strength and burn more energy
          - Stair climbing on leash with mixed patterns
          - Fetch races and hide-and-seek with toys or kibble
          - Tag games at dog parks, backyards, or indoors for cardio workouts
          - Obstacle courses with hurdles, tunnels, and slalom setups
          - Swimming or hydrotherapy — ideal for dogs with arthritis or back problems

        Important safety note (Hill's Pet): avoid using sticks as fetch toys
        due to splinter and injury risks.

        Duration principle (WebMD): spending 10-15 minutes outside exploring is better
        than skipping activity because you don't feel like you have enough time.
        Quality is more important than quantity.
        Dogs should have the opportunity to exercise multiple times each day when possible.

        Age-based adjustments (WebMD):
          - Older dogs: low-impact activity like walking
          - Young puppies: may be very active but need supervision to avoid injuries
          - Toy selection should match the dog's age and strength

        Nutrition note (WebMD): proper nutrition gives dogs more energy to play.
        An unusually lethargic or disinterested dog may need veterinary consultation.
        """
    },
    {
        "id": "dog_exercise_mistakes",
        "title": "Common Dog Exercise Mistakes to Avoid",
        "source": "Dr. Peter Dobias - peterdobias.com/blogs/blog/76674565-one-of-the-most-common-mistakes-people-make-when-exercising-their-dogs",
        "content": """
        Source: Dr. Peter Dobias (peterdobias.com)

        Most common mistake: excessive repetitive chasing (ball, frisbee).
        Dogs in nature never chase 50-100 objects in 30 minutes.
        Repetitive ball and frisbee chasing causes slipping, back injuries, and
        long-term nerve damage, which can lead to chronic pain and premature aging.

        Recommended safe activities:
          - Hiking and walking on trails — described as the best form of exercise for dogs
          - Moving across varied terrain with rocks and obstacles builds strength and balance
          - Hide-and-seek with toys instead of repetitive ball throwing
          - Chase games where the owner chases the dog (not the other way around)
          - Teaching navigation skills: logs, tunnels, weaving

        Frequency: dogs should exercise twice daily in all weather conditions.
        Activity should mimic natural roaming and exploration patterns.

        Senior dogs: uphill walking helps maintain strength and mobility.
        Progressive stiffness is a sign of arthritis — consult a vet for natural treatment options.
        Repetitive chasing injuries accumulate over time even if not immediately visible.
        """
    }
]


class VectorStore:
    """
    Simple in-memory vector store using sentence embeddings.
    Supports basic semantic search over pet care documents.
    """
    
    def __init__(self):
        """Initialize vector store. Embeddings loaded lazily on first query."""
        self.documents = PET_CARE_DOCUMENTS
        self.embeddings = None
        self.model = None
    
    def _load_model(self):
        """Load sentence transformer model for embeddings (lazy loading)."""
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            # Pre-compute embeddings for all documents
            self.embeddings = {
                doc["id"]: self.model.encode(doc["title"] + " " + doc["content"])
                for doc in self.documents
            }
    
    def retrieve(self, query: str, top_k: int = 3) -> list:
        """
        Retrieve most relevant documents for a query using semantic similarity.
        
        Args:
            query: Search query about pet care
            top_k: Number of documents to return
            
        Returns:
            List of most relevant documents sorted by similarity score
        """
        self._load_model()
        query_embedding = self.model.encode(query)
        
        # Compute similarity scores
        scores = []
        for doc_id, doc_embedding in self.embeddings.items():
            # Simple cosine similarity
            similarity = (query_embedding @ doc_embedding) / (
                (query_embedding @ query_embedding) ** 0.5 * 
                (doc_embedding @ doc_embedding) ** 0.5
            )
            doc = next(d for d in self.documents if d["id"] == doc_id)
            scores.append((similarity, doc))
        
        # Sort by similarity and return top-k
        scores.sort(reverse=True)
        return [doc for _, doc in scores[:top_k]]


class PetCareRetriever:
    """
    RAG Retriever: Fetches relevant pet care knowledge given a pet query.
    Combines simple keyword matching with semantic search.
    """
    
    def __init__(self):
        """Initialize retriever with vector store."""
        self.vector_store = VectorStore()
    
    def retrieve(self, pet_species: str, pet_age: int, query_topic: str) -> str:
        """
        Retrieve relevant pet care guidelines.
        
        Args:
            pet_species: "dog" or "cat"
            pet_age: Age in years
            query_topic: What we're looking for (e.g., "exercise", "feeding", "grooming")
            
        Returns:
            Combined context from relevant documents
        """
        # Build semantic query
        query = f"{pet_species} {query_topic} age {pet_age} years"
        
        # Retrieve similar documents
        relevant_docs = self.vector_store.retrieve(query, top_k=2)
        
        # Combine content for context
        context = "\n\n".join([
            f"**{doc['title']}**\n{doc['content']}" 
            for doc in relevant_docs
        ])
        
        return context
