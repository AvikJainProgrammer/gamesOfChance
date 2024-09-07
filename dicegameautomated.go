package main

import (
	"fmt"
	"math/rand"
	"time"
)

// DiceGame structure
type DiceGame struct {
	winCount   int
	lossCount  int
	betAmount  float64
	winChance  float64
	balance    float64
	houseEdge  float64
	multiplier float64
	lastBetWon bool
}

// DiceGameAutomated structure inheriting from DiceGame
type DiceGameAutomated struct {
	DiceGame
	originalBetAmount float64
}

// Initialize DiceGame with balance and house edge
func (dg *DiceGame) Init(balance, houseEdge float64) {
	dg.balance = balance
	dg.houseEdge = houseEdge
	dg.winChance = 50.0
	dg.setMultiplierOnChance(dg.winChance)
}

// Set bet amount
func (dg *DiceGame) SetBetAmount(betAmount float64) {
	dg.betAmount = betAmount
}

// Set win chance and update multiplier
func (dg *DiceGame) SetWinChance(winChance float64) {
	dg.winChance = winChance
	dg.setMultiplierOnChance(winChance)
}

// Calculate and set the multiplier based on win chance
func (dg *DiceGame) setMultiplierOnChance(winChance float64) {
	dg.multiplier = (99.0 / winChance) * (1.0 - dg.houseEdge)
}

// Simulate rolling a dice
func (dg *DiceGame) RollDice() float64 {
	return rand.Float64() * 100.0
}

// Handle win scenario
func (dg *DiceGame) Win() float64 {
	winning := dg.betAmount * (dg.multiplier - 1)
	dg.balance += winning
	dg.winCount++
	return winning
}

// Handle loss scenario
func (dg *DiceGame) Lose() float64 {
	loss := dg.betAmount
	dg.balance -= loss
	dg.lossCount++
	return loss
}

// Check if a bet can be placed
func (dg *DiceGame) CanBet() bool {
	return dg.betAmount <= dg.balance
}

// Execute a bet
func (dg *DiceGame) Bet() {
	if !dg.CanBet() {
		panic("Cannot place bet")
	}

	diceValue := dg.RollDice()
	if diceValue < dg.winChance {
		dg.lastBetWon = true
		dg.Win()
	} else {
		dg.lastBetWon = false
		dg.Lose()
	}
}

// Initialize DiceGameAutomated with balance and house edge
func (dga *DiceGameAutomated) Init(balance, houseEdge float64) {
	dga.DiceGame.Init(balance, houseEdge)
	dga.originalBetAmount = dga.betAmount
}

// Automated betting with multipliers based on win/loss
func (dga *DiceGameAutomated) AutoBet(betCount int, lastWinMultiplier, lastLossMultiplier *float64) {
	for i := 0; i < betCount; i++ {
		if !dga.CanBet() {
			break
		}

		dga.Bet()

		if dga.lastBetWon {
			if lastWinMultiplier == nil {
				dga.betAmount = dga.originalBetAmount
			} else {
				dga.betAmount *= *lastWinMultiplier
			}
		} else {
			if lastLossMultiplier == nil {
				dga.betAmount = dga.originalBetAmount
			} else {
				dga.betAmount *= *lastLossMultiplier
			}
		}
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	profit := 0.0
	profitCount := 0
	lossCount := 0

	balanceAmount := 10000.0
	betAmount := 0.01
	winChances := 75.0
	betCount := 100
	lossMultiplier := 5.0

	for i := 0; i < 10000; i++ {
		var dga DiceGameAutomated
		dga.Init(balanceAmount, 0.0)
		dga.SetBetAmount(betAmount)
		dga.SetWinChance(winChances)
		dga.AutoBet(betCount, nil, &lossMultiplier)

		profit += (dga.balance - balanceAmount)
		if dga.balance < balanceAmount {
			lossCount++
		} else if dga.balance > balanceAmount {
			profitCount++
		}
	}

	fmt.Println("____")
	fmt.Printf("Profit: %.2f\n", profit)
	fmt.Printf("Profit percentage: %.5f%%\n", (profit/balanceAmount)*100)
	fmt.Println("Profit count:", profitCount)
	fmt.Println("Loss count:", lossCount)
}
