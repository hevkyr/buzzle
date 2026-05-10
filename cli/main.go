// buzzle/cli/main.go
// Blazing-fast CLI client for the buzzle API.
//
// Usage:
//   buzzle generate
//   buzzle generate --count 5
//   buzzle generate --json
//   buzzle generate --seed 42
//   buzzle stats

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

const (
	defaultAPI = "http://localhost:8000"
	version    = "1.0.0"
	banner     = `
  ██████╗ ██╗   ██╗███████╗███████╗██╗     ███████╗
  ██╔══██╗██║   ██║╚══███╔╝╚══███╔╝██║     ██╔════╝
  ██████╔╝██║   ██║  ███╔╝   ███╔╝ ██║     █████╗
  ██╔══██╗██║   ██║ ███╔╝   ███╔╝  ██║     ██╔══╝
  ██████╔╝╚██████╔╝███████╗███████╗███████╗███████╗
  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝
`
)

// ── Types ─────────────────────────────────────────────────────────────────────

type Phrase struct {
	Phrase      string `json:"phrase"`
	Score       int    `json:"score"`
	Category    string `json:"category"`
	GeneratedAt string `json:"generated_at"`
}

type Stats struct {
	Total        int     `json:"total_phrases_generated"`
	Uptime       float64 `json:"uptime_seconds"`
	MostUsedNoun string  `json:"most_used_noun"`
	Version      string  `json:"engine_version"`
}

// ── HTTP helpers ──────────────────────────────────────────────────────────────

func fetch(url string) ([]byte, error) {
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("could not reach buzzle API at %s\n→ is it running? try: uvicorn main:app", url)
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// ── Commands ──────────────────────────────────────────────────────────────────

func cmdGenerate(api string, count int, seed int, asJSON bool) {
	url := fmt.Sprintf("%s/phrase?count=%d", api, count)
	if seed >= 0 {
		url += fmt.Sprintf("&seed=%d", seed)
	}

	body, err := fetch(url)
	if err != nil {
		fmt.Fprintln(os.Stderr, "✗", err)
		os.Exit(1)
	}

	if asJSON {
		fmt.Println(string(body))
		return
	}

	// Single phrase
	if count == 1 {
		var p Phrase
		if err := json.Unmarshal(body, &p); err != nil {
			fmt.Fprintln(os.Stderr, "✗ parse error:", err)
			os.Exit(1)
		}
		printPhrase(p, 1)
		return
	}

	// Multiple phrases
	var phrases []Phrase
	if err := json.Unmarshal(body, &phrases); err != nil {
		fmt.Fprintln(os.Stderr, "✗ parse error:", err)
		os.Exit(1)
	}
	for i, p := range phrases {
		printPhrase(p, i+1)
	}
}

func printPhrase(p Phrase, n int) {
	stars := scoreToStars(p.Score)
	fmt.Printf("\n  %d. \033[1;36m%s\033[0m\n", n, p.Phrase)
	fmt.Printf("     %s  \033[2m[%s · score: %d/100]\033[0m\n", stars, p.Category, p.Score)
}

func scoreToStars(score int) string {
	stars := score / 20
	out := ""
	for i := 0; i < 5; i++ {
		if i < stars {
			out += "★"
		} else {
			out += "☆"
		}
	}
	return out
}

func cmdStats(api string) {
	body, err := fetch(api + "/stats")
	if err != nil {
		fmt.Fprintln(os.Stderr, "✗", err)
		os.Exit(1)
	}

	var s Stats
	if err := json.Unmarshal(body, &s); err != nil {
		fmt.Fprintln(os.Stderr, "✗ parse error:", err)
		os.Exit(1)
	}

	fmt.Println("\n  \033[1mBuzzle API Stats\033[0m")
	fmt.Println("  ─────────────────────────────")
	fmt.Printf("  📊 Total phrases generated : %d\n", s.Total)
	fmt.Printf("  ⏱  Uptime                  : %.1fs\n", s.Uptime)
	fmt.Printf("  🏆 Most used noun           : %s\n", s.MostUsedNoun)
	fmt.Printf("  🔧 Engine version           : %s\n\n", s.Version)
}

// ── Main ──────────────────────────────────────────────────────────────────────

func main() {
	// Subcommands
	genCmd := flag.NewFlagSet("generate", flag.ExitOnError)
	genCount := genCmd.Int("count", 1, "number of phrases to generate (max 20)")
	genSeed := genCmd.Int("seed", -1, "RNG seed for reproducibility (-1 = random)")
	genJSON := genCmd.Bool("json", false, "output raw JSON")
	genAPI := genCmd.String("api", defaultAPI, "buzzle API base URL")

	statsCmd := flag.NewFlagSet("stats", flag.ExitOnError)
	statsAPI := statsCmd.String("api", defaultAPI, "buzzle API base URL")

	if len(os.Args) < 2 {
		fmt.Print(banner)
		fmt.Printf("  buzzle v%s — motivational nonsense as a service\n\n", version)
		fmt.Println("  Commands:")
		fmt.Println("    generate   Generate phrase(s)")
		fmt.Println("    stats      Show API statistics")
		fmt.Println("    version    Print version\n")
		fmt.Println("  Examples:")
		fmt.Println("    buzzle generate")
		fmt.Println("    buzzle generate --count 5")
		fmt.Println("    buzzle generate --seed 42 --json")
		fmt.Println("    buzzle stats\n")
		os.Exit(0)
	}

	switch os.Args[1] {
	case "generate", "gen", "g":
		genCmd.Parse(os.Args[2:])
		cmdGenerate(*genAPI, *genCount, *genSeed, *genJSON)
	case "stats", "s":
		statsCmd.Parse(os.Args[2:])
		cmdStats(*statsAPI)
	case "version", "v", "--version", "-v":
		fmt.Printf("buzzle v%s\n", version)
	default:
		fmt.Fprintf(os.Stderr, "✗ unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
