Feature: General Challenge
	Prize: $15,000 Cash prize

	Scenario Outline: Complete the challenge
		Given the challenge is General Challenge
		When the participant attempts the challenge
		Then they should either win or lose

	Examples:
		| challenge_result |
		| win              |
		| lose             |
