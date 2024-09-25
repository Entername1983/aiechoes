INITIAL_CONTEXT = {
    "rules": {
        "dialogue": "Maintain each character's unique voice and speech patterns.",
        "foreshadowing": "Subtly hint at future events without revealing them outright.",
        "plotConsistency": "Ensure that new developments align with established plot points and character motivations.",
        "locationDescription": "When introducing new locations, include sensory details.",
        "characterIntroduction": "New major characters should be introduced gradually and with purpose.",
        "style": "",
    },
    "themes": ["Friendship", "Adventure", "Self-Discovery", "Reconciliation", "Mystery"],
    "setting": {
        "timeline": [
            {"id": "EV1", "date": "2023-01-01", "event": "John discovers an old map in his attic."},
            {
                "id": "EV2",
                "date": "2023-01-05",
                "event": "Emily contacts John after learning about the map.",
            },
        ],
        "locations": [
            {
                "id": "LC1",
                "name": "St. John's, Newfoundland",
                "history": ["Founded in 1497", "Survived the Great Fire of 1892"],
                "coordinates": {"latitude": "47.5615", "longitude": "-52.7126"},
                "description": "A coastal city with a rich history.",
                "significance": "John's hometown and starting point of the adventure.",
            },
            {
                "id": "LC2",
                "name": "The Old Lighthouse",
                "builtYear": "1850",
                "description": "An abandoned lighthouse rumored to be haunted.",
                "significance": "Key location where the first clue is found.",
                "currentCondition": "Dilapidated but structurally sound",
            },
        ],
        "timePeriod": "Present Day",
    },
    "subplots": [
        {
            "id": "SP1",
            "title": "John's Reconciliation with His Father",
            "status": "Ongoing",
            "progress": "John has written a letter but hasn't sent it yet.",
            "description": "John seeks to mend his relationship with his estranged father, Robert.",
            "dependencies": ["P1"],
            "charactersInvolved": ["C1", "C3"],
        }
    ],
    "narration": {
        "narrators": [
            {
                "id": "N1",
                "name": "Third-Person Omniscient",
                "characterId": "none",
                "rules": {
                    "access": "Can reveal thoughts and feelings of any character",
                    "limitations": "Should not reveal future plot twists directly",
                    "perspective": "All-knowing",
                },
            },
            {
                "id": "N2",
                "characterId": "C1",
                "name": "First-Person (John)",
                "rules": {
                    "access": "Only John's thoughts and observations",
                    "limitations": "Cannot know other characters' internal thoughts unless expressed",
                    "perspective": "Limited to John's experiences",
                },
            },
        ],
        "narrationRules": {
            "switching": "Narrator can switch only at chapter breaks or significant plot points",
            "consistency": "Maintain the same narrator within a scene",
        },
        "currentNarrator": "N1",
    },
    "mainPlots": [
        {
            "id": "P1",
            "date": "2023-01-01",
            "title": "Discovery of the Map",
            "status": "Completed",
            "description": "John finds an old map hidden in his attic, sparking the beginning of his adventure.",
            "dependencies": [],
            "relatedSubplots": ["John's family history", "The legend of the lost treasure"],
            "charactersInvolved": ["C1"],
        },
        {
            "id": "P2",
            "date": "2023-01-05",
            "title": "Reunion with Emily",
            "status": "Completed",
            "description": "Emily reaches out to John to collaborate on deciphering the map.",
            "dependencies": ["P1"],
            "relatedSubplots": ["Emily's career ambitions", "Their past collaboration"],
            "charactersInvolved": ["C1", "C2"],
        },
        {
            "id": "P3",
            "date": "2023-01-10",
            "title": "Exploring the Old Lighthouse",
            "status": "In Progress",
            "description": "John and Emily decide to explore the Old Lighthouse at midnight, believing it holds clues.",
            "dependencies": ["P2"],
            "relatedSubplots": ["Local legends", "Emily's skepticism"],
            "charactersInvolved": ["C1", "C2"],
        },
    ],
    "subPlots": [],
    "currentContext": {
        "time": "2023-01-10 23:50",
        "summary": "John and Emily stand before the looming structure of the Old Lighthouse, preparing to enter and search for clues.",
        "weather": "Foggy with a slight drizzle",
        "location": {
            "locationId": "LC1",
            "name": "Entrance of the Old Lighthouse",
            "details": "A narrow path leads to the entrance, flanked by overgrown bushes.",
        },
        "currentNarrator": "N1",
        "emotionalStates": {
            "C1": "Anxious but excited",
            "C2": "Determined with a hint of skepticism",
        },
        "mainPlot": "P1",
        "subPlot": "SP1",
        "charactersPresent": [
            {"characterId": "C1", "name": "John Smith"},
            {"characterId": "C2", "name": "Emily Turner"},
        ],
        "characterStates": {"C1": "Normal", "C2": "Normal"},
        "narrator": "N1",
    },
    "characters": {
        "mainCharacters": [
            {
                "id": "C1",
                "age": "28",
                "firstName": "John ",
                "lastName": "Smith",
                "nickname": "None",
                "goals": ["Find the lost treasure", "Reconcile with his father"],
                "traits": ["curious", "brave", "introverted"],
                "background": {
                    "family": {
                        "father": "Robert Smith (estranged)",
                        "mother": "Mary Smith (deceased)",
                    },
                    "history": "Lost his mother at age 18; estranged from his father since childhood.",
                    "hometown": "St. John's, Newfoundland",
                    "education": "Bachelor's degree in Mechanical Engineering",
                    "occupation": "Engineer",
                },
                "relationships": [
                    {
                        "history": "Met Emily during university years; collaborated on projects.",
                        "characterId": "C2",
                        "currentStatus": "Close friends",
                        "relationshipType": "Friend",
                    },
                    {
                        "history": "Father left when John was 10; minimal contact since.",
                        "characterId": "C3",
                        "currentStatus": "Estranged but seeking reconciliation",
                        "relationshipType": "Father",
                    },
                ],
            },
            {
                "id": "C2",
                "age": "25",
                "firstName": "Emily",
                "lastName": "Turner",
                "nickname": "None",
                "goals": ["Uncover the conspiracy", "Achieve a breakthrough in her career"],
                "traits": ["outgoing", "determined", "clever"],
                "background": {
                    "family": {"father": "George Turner", "mother": "Linda Turner"},
                    "history": "Moved to St. John's for a major story.",
                    "hometown": "Toronto, Canada",
                    "education": "Master's degree in Journalism",
                    "occupation": "Investigative Journalist",
                },
                "relationships": [
                    {
                        "history": "Met John at university; maintained friendship over the years.",
                        "characterId": "C1",
                        "currentStatus": "Trusted confidant",
                        "relationshipType": "Friend",
                    },
                    {
                        "history": "Competes with Alex Monroe for top stories.",
                        "characterId": "C4",
                        "currentStatus": "Competitive but respectful",
                        "relationshipType": "Professional Rival",
                    },
                ],
            },
        ],
        "secondaryCharacters": [],
    },
}
