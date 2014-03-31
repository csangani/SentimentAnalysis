package androidcommentscraper;

import com.gc.android.market.api.MarketSession;
import com.gc.android.market.api.MarketSession.Callback;
import com.gc.android.market.api.model.Market.AppsRequest;
import com.gc.android.market.api.model.Market.AppsRequest.OrderType;
import com.gc.android.market.api.model.Market.AppsResponse;
import com.gc.android.market.api.model.Market.ResponseContext;

/**
 *
 * @author Chirag Sangani
 */
public class AppIDScraper {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws InterruptedException {
        MarketSession session = SessionSetup.Now();

        String query = "terraria";
        AppsRequest appsRequest = AppsRequest.newBuilder()
                .setQuery(query)
                .setOrderType(OrderType.NEWEST)
                .setStartIndex(0).setEntriesCount(10)
                .build();

        session.append(appsRequest, new Callback<AppsResponse>() {
            @Override
            public void onResult(ResponseContext context, AppsResponse response) {
                System.out.println(response);
            }
        });

        session.flush();
    }
}
