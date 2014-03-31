/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package androidcommentscraper;

import com.gc.android.market.api.MarketSession;

/**
 *
 * @author Chirag
 */
public class SessionSetup {

    public static MarketSession Now() {
        MarketSession session = new MarketSession();
        session.login("yourid@gmail.com", "yourpassword");
        return session;
    }
}
