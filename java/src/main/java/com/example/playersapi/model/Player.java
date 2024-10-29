package com.example.playersapi.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Player {
    
    private String playerID;
    private String nameFirst;
    private String nameLast;

    // Optionally, add any other fields from your CSV file and map them here
}
