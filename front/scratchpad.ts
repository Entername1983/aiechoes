const struct = {
    "story": {
      "settings": {
        "timePeriod": "Present Day",
        "timeline": [
          {
            "date": "2023-01-01",
            "event": "John discovers an old map in his attic."
          },
          {
            "date": "2023-01-05",
            "event": "Emily contacts John after learning about the map."
          }
          // Additional events can be added here
        ],
        "locations": [
          {
            "name": "St. John's, Newfoundland",
            "description": "A coastal city with a rich history.",
            "significance": "John's hometown and starting point of the adventure.",
            "coordinates": { "latitude": 47.5615, "longitude": -52.7126 },
            "history": ["Founded in 1497", "Survived the Great Fire of 1892"]
          },
          {
            "name": "The Old Lighthouse",
            "description": "An abandoned lighthouse rumored to be haunted.",
            "significance": "Key location where the first clue is found.",
            "builtYear": 1850,
            "currentCondition": "Dilapidated but structurally sound"
          }
          // More locations can be added here
        ]
      },
      "mainCharacters": [
        {
          "id": "C1",
          "name": "John Smith",
          "age": 28,
          "background": {
            "occupation": "Engineer",
            "hometown": "St. John's, Newfoundland",
            "family": {
              "mother": "Mary Smith (deceased)",
              "father": "Robert Smith (estranged)"
            },
            "education": "Bachelor's degree in Mechanical Engineering",
            "history": "Lost his mother at age 18; estranged from his father since childhood."
          },
          "traits": ["curious", "brave", "introverted"],
          "goals": ["Find the lost treasure", "Reconcile with his father"],
          "relationships": [
            {
              "characterId": "C2",
              "relationshipType": "Friend",
              "history": "Met Emily during university years; collaborated on projects.",
              "currentStatus": "Close friends"
            },
            {
              "characterId": "C3",
              "relationshipType": "Father",
              "history": "Father left when John was 10; minimal contact since.",
              "currentStatus": "Estranged but seeking reconciliation"
            },
            // Additional relationships can be added here
          ]
        },
        {
          "id": "C2",
          "name": "Emily Turner",
          "age": 25,
          "background": {
            "occupation": "Investigative Journalist",
            "hometown": "Toronto, Canada",
            "family": {
              "mother": "Linda Turner",
              "father": "George Turner"
            },
            "education": "Master's degree in Journalism",
            "history": "Moved to St. John's for a major story."
          },
          "traits": ["outgoing", "determined", "clever"],
          "goals": ["Uncover the conspiracy", "Achieve a breakthrough in her career"],
          "relationships": [
            {
              "characterId": "C1",
              "relationshipType": "Friend",
              "history": "Met John at university; maintained friendship over the years.",
              "currentStatus": "Trusted confidant"
            },
            {
              "characterId": "C4",
              "relationshipType": "Professional Rival",
              "history": "Competes with Alex Monroe for top stories.",
              "currentStatus": "Competitive but respectful"
            },
            // Additional relationships can be added here
          ]
        },
        // More characters can be added here
      ],
      "plotPoints": [
        {
          "id": "P1",
          "title": "Discovery of the Map",
          "description": "John finds an old map hidden in his attic, sparking the beginning of his adventure.",
          "status": "Completed",
          "date": "2023-01-01",
          "charactersInvolved": ["C1"],
          "dependencies": [],
          "relatedSubplots": ["John's family history", "The legend of the lost treasure"]
        },
        {
          "id": "P2",
          "title": "Reunion with Emily",
          "description": "Emily reaches out to John to collaborate on deciphering the map.",
          "status": "Completed",
          "date": "2023-01-05",
          "charactersInvolved": ["C1", "C2"],
          "dependencies": ["P1"],
          "relatedSubplots": ["Emily's career ambitions", "Their past collaboration"]
        },
        {
          "id": "P3",
          "title": "Exploring the Old Lighthouse",
          "description": "John and Emily decide to explore the Old Lighthouse at midnight, believing it holds clues.",
          "status": "In Progress",
          "date": "2023-01-10",
          "charactersInvolved": ["C1", "C2"],
          "dependencies": ["P2"],
          "relatedSubplots": ["Local legends", "Emily's skepticism"]
        },
        // Additional plot points can be added here
      ],
      "subplots": [
        {
          "id": "SP1",
          "title": "John's Reconciliation with His Father",
          "description": "John seeks to mend his relationship with his estranged father, Robert.",
          "status": "Ongoing",
          "charactersInvolved": ["C1", "C3"],
          "dependencies": ["P1"],
          "progress": "John has written a letter but hasn't sent it yet."
        },
        // More subplots can be added here
      ],
      "themes": ["Friendship", "Adventure", "Self-Discovery", "Reconciliation", "Mystery"],
      "narration": {
        "narrators": [
          {
            "id": "N1",
            "name": "Third-Person Omniscient",
            "rules": {
              "perspective": "All-knowing",
              "access": "Can reveal thoughts and feelings of any character",
              "limitations": "Should not reveal future plot twists directly"
            }
          },
          {
            "id": "N2",
            "name": "First-Person (John)",
            "rules": {
              "perspective": "Limited to John's experiences",
              "access": "Only John's thoughts and observations",
              "limitations": "Cannot know other characters' internal thoughts unless expressed"
            }
          }
          // Additional narrators can be added here
        ],
        "currentNarrator": "N1",
        "narrationRules": {
          "switching": "Narrator can switch only at chapter breaks or significant plot points",
          "consistency": "Maintain the same narrator within a scene"
        }
      },
      "currentContext": {
        "time": "2023-01-10 23:50",
        "location": "Entrance of the Old Lighthouse",
        "weather": "Foggy with a slight drizzle",
        "charactersPresent": ["C1", "C2"],
        "summary": "John and Emily stand before the looming structure of the Old Lighthouse, preparing to enter and search for clues.",
        "emotionalStates": {
          "C1": "Anxious but excited",
          "C2": "Determined with a hint of skepticism"
        },
        "currentNarrator": "N1"
      },
      "rules": {
        "characterIntroduction": "New major characters should be introduced gradually and with purpose.",
        "locationDescription": "When introducing new locations, include sensory details.",
        "dialogue": "Maintain each character's unique voice and speech patterns.",
        "plotConsistency": "Ensure that new developments align with established plot points and character motivations.",
        "foreshadowing": "Subtly hint at future events without revealing them outright."
      }
    }
  }
  