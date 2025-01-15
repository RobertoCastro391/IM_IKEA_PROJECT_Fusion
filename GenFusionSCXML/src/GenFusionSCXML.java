/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

 import java.io.IOException;
 import scxmlgen.Fusion.FusionGenerator;
 //import FusionGenerator;
 
 import Modalities.Output;
 import Modalities.Speech;
 import Modalities.Touch;
 
 /**
  *
  * @author nunof
  */
 public class GenFusionSCXML {
 
     /**
      * @param args the command line arguments
      */
     public static void main(String[] args) throws IOException {
 
     FusionGenerator fg = new FusionGenerator();
     
 
     fg.Single(Speech.SEARCH_PRODUCT_CAMAS, Output.SEARCH_PRODUCT_CAMAS);
     fg.Single(Speech.SEARCH_PRODUCT_CADEIRAS, Output.SEARCH_PRODUCT_CADEIRAS);
     fg.Single(Speech.SEARCH_PRODUCT_ARMARIOS, Output.SEARCH_PRODUCT_ARMARIOS);
     fg.Single(Speech.SEARCH_PRODUCT_ESTANTES, Output.SEARCH_PRODUCT_ESTANTES);
     fg.Single(Speech.SEARCH_PRODUCT_SOFAS, Output.SEARCH_PRODUCT_SOFAS);
     
     fg.Build("fusion.scxml");
         
     }
     
 }
 