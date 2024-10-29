import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/players")
public class PlayerController {

    private final SparkSession sparkSession;
    private final Dataset<Row> playersDF;

    // Constructor for initializing Spark session and loading data
    public PlayerController() {
        this.sparkSession = SparkSession.builder().appName("PlayersAPI").master("local").getOrCreate();
        String filePath = "/path/to/your/player.csv"; // Adjust the path to your file location
        this.playersDF = sparkSession.read().option("header", "true").csv(filePath);
    }

    // Endpoint to get all players with optional pagination
    @GetMapping
    public List<Map<String, Object>> getAllPlayers(@RequestParam Optional<Integer> skip, @RequestParam Optional<Integer> limit) {
        List<Row> playersList = playersDF.select("playerID", "nameFirst", "nameLast").collectAsList();

        int start = skip.orElse(0);
        int end = limit.map(l -> Math.min(start + l, playersList.size())).orElse(playersList.size());

        return playersList.subList(start, end).stream()
                .map(row -> row.getValuesMap(row.schema().fieldNames()))
                .collect(Collectors.toList());
    }

    // Endpoint to get a single player by ID
    @GetMapping("/{playerID}")
    public Map<String, Object> getPlayerById(@PathVariable String playerID) {
        List<Row> players = playersDF.filter(playersDF.col("playerID").equalTo(playerID)).collectAsList();
        
        if (players.isEmpty()) {
            throw new PlayerNotFoundException("Player not found");
        }
        
        return players.get(0).getValuesMap(players.get(0).schema().fieldNames());
    }
}
