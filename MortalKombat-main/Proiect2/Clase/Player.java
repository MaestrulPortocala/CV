package Proiect2.Clase;

public class Player {
    private String name;
    final private int health=100;
    static public int punch=5;
    static public int elbow=10;
    static public int kick=15;
    static public int headbutt=20;
    public void setName(String nume){
        name=nume;
    }
    public String getName(){
        return name;
    }

    public int getHealth(){
        return health;
    }
    public String toString(){
        return "Each player has "+health+" health and these attack moves:\n1)Punch does "+punch+" damage and is always landing\n2)Elbow does "+elbow+" damage and has a 1/2 chance of landing\n3)Kick does "+kick+" damage and has a 1/3 chance of landing\n4)Headbutt does "+headbutt+" damage and has a 1/4 chance of landing\nWhoever drains the opponent's life to 0 first wins by FATALITY \nENJOY:)";
    }
   }