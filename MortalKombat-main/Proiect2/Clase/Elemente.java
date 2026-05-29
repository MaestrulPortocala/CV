package Proiect2.Clase;

import javax.swing.*;

public class Elemente {
    static public Music musicPlayer;
    static public int x1, x2, y1, y2;
   static public boolean play=true, dodged=false;
   static public JButton[] butoane=new JButton[12];
   static public JLabel[] labels=new JLabel[15];
   static public JPanel[] panels= new JPanel[5];
   static {
       Player p = new Player();
       butoane = Menu.configureButton(butoane);
       butoane[0].setText("Fight");
       butoane[1].setText("Rules");
       butoane[2].setText("Credits");
       butoane[3].setText("Exit");
       butoane[4].setText("KOMBAAAT!!!");
       butoane[5].setText("BRAVO!!!");
       butoane[6].setText("Punch");
       butoane[7].setText("Elbow");
       butoane[8].setText("Kick");
       butoane[9].setText("Headbutt");
       butoane[10].setText("ok");
       butoane[11].setText("Back");
       Menu.configureLabels(labels, 0, 4, 100);
       Menu.configureLabels(labels, 4, 7, 60);
       Menu.configureLabels(labels, 7, 10, 25);
       Menu.configureLabels(labels, 10, 12, 60);
       labels[0].setText("MORTAL KOMBAT ");
       labels[1].setText("DUMBRAVIOARA EDITION");
       labels[2].setText("FIGHT!!! ");
       labels[3].setText("FATALITY!!! ");
       labels[4].setText("RULES ");
       labels[5].setText("EU! ");
       labels[6].setText("");
       labels[7].setText("<html>" + p.toString().replace("\n", "<br>") + "</html>");
       labels[8].setText("Name for player 1: ");
       labels[9].setText("Name for player 2: ");
       labels[10].setText("");
       labels[11].setText("");
       for(int i=12; i<15; ++i){
           labels[i]=new JLabel();
      }
       panels=Menu.init_panel(panels);
   }
}
