/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.IOException;
import scxmlgen.Fusion.FusionGenerator;
//import FusionGenerator;
import Modalities.Gestures;
import Modalities.Output;
import Modalities.Speech;

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


        // Single Voice

        fg.Single(Speech.OPEN_WEBSITE, Output.OPEN_WEBSITE);
        fg.Single(Speech.SHOW_FAVORITES, Output.SHOW_FAVORITES);
        fg.Single(Speech.SHOW_CART, Output.SHOW_CART);
        fg.Single(Speech.ADD_PRODUCT_CART, Output.ADD_PRODUCT_CART);
        fg.Single(Speech.ADD_PRODUCT_FAVORITES, Output.ADD_PRODUCT_FAVORITES);
        fg.Single(Speech.REMOVE_PRODUCT_CART, Output.REMOVE_PRODUCT_CART);
        fg.Single(Speech.REMOVE_PRODUCT_FAVORITES, Output.REMOVE_PRODUCT_FAVORITES);
        fg.Single(Speech.SHOW_MORE, Output.SHOW_MORE);

        fg.Single(Speech.SEARCH_PRODUCT_CAMAS, Output.SEARCH_PRODUCT_CAMAS);
        fg.Single(Speech.SEARCH_PRODUCT_CADEIRAS, Output.SEARCH_PRODUCT_CADEIRAS);
        fg.Single(Speech.SEARCH_PRODUCT_ARMARIOS, Output.SEARCH_PRODUCT_ARMARIOS);
        fg.Single(Speech.SEARCH_PRODUCT_ESTANTES, Output.SEARCH_PRODUCT_ESTANTES);
        fg.Single(Speech.SEARCH_PRODUCT_SOFAS, Output.SEARCH_PRODUCT_SOFAS);
        fg.Single(Speech.SEARCH_PRODUCT_MESAS, Output.SEARCH_PRODUCT_MESAS);

        fg.Single(Speech.SCROLL_UP, Output.SCROLL_UP);
        fg.Single(Speech.SCROLL_DOWN, Output.SCROLL_DOWN);

        fg.Single(Speech.GO_BACK, Output.GO_BACK);
        fg.Single(Speech.MAIN_PAGE, Output.MAIN_PAGE);
        
        // Single Gestures
        fg.Single(Gestures.SCROLL_UP, Output.SCROLL_UP);
        fg.Single(Gestures.SCROLL_DOWN, Output.SCROLL_DOWN);
        fg.Single(Gestures.GO_BACK, Output.GO_BACK);
        fg.Single(Gestures.MAIN_PAGE, Output.MAIN_PAGE);
        fg.Single(Gestures.CLOSE_WEB, Output.CLOSE_WEB);
        fg.Single(Gestures.GO_UP, Output.GO_UP);
        fg.Single(Gestures.GO_DOWN, Output.GO_DOWN);
        fg.Single(Gestures.GO_LEFT, Output.GO_LEFT);
        fg.Single(Gestures.GO_RIGHT, Output.GO_RIGHT);

        fg.Build("fusion.scxml");

    }

}
