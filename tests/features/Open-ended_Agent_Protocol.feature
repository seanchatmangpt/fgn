Feature: Open-ended Agent Protocol
	Prize: $3,000

	Scenario Outline: Complete the challenge
		Given the challenge is Open-ended Agent Protocol
		When the participant attempts the challenge
		Then they should either win or lose

	Examples:
		| challenge_result |
		| win              |
		| lose             |
