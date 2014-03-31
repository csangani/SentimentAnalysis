/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package androidcommentscraper;

import com.gc.android.market.api.MarketSession;
import com.gc.android.market.api.MarketSession.Callback;
import com.gc.android.market.api.model.Market;
import com.gc.android.market.api.model.Market.Comment;
import com.gc.android.market.api.model.Market.CommentsRequest;
import com.gc.android.market.api.model.Market.CommentsResponse;
import com.gc.android.market.api.model.Market.ResponseContext;
import com.google.protobuf.Descriptors.FieldDescriptor;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import org.json.simple.JSONValue;

/**
 *
 * @author Chirag
 */
public class CommentsScraper {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws InterruptedException, FileNotFoundException {
        MarketSession session = SessionSetup.Now();
        final List<Map<String, Object>> comments = new LinkedList<>();
        final List<Integer> exceptionCount = new LinkedList<>();
        
        for (int i = 0; i < 10; i++) {
            exceptionCount.add(0);
        }
        
        for (int i = 0; exceptionCount.size() > 0; i += 10) {

            CommentsRequest commentsRequest = CommentsRequest.newBuilder()
                    .setAppId("v2:com.Relmtech.Remote:1:47")
                    .setStartIndex(i)
                    .setEntriesCount(10)
                    .build();

            session.append(commentsRequest, new Callback<CommentsResponse>() {
                @Override
                public void onResult(ResponseContext context, CommentsResponse response) {
                    try {
                        for (Comment comment : response.getCommentsList()) {
                            Map<String, Object> c = new HashMap<>();
                            for (FieldDescriptor key : comment.getAllFields().keySet()) {
                                c.put(key.getName(), comment.getAllFields().get(key));
                            }
                            comments.add(c);
                        }
                    } catch (Exception e) {
                        exceptionCount.remove(0);
                    }
                }
            });

            System.out.println(comments.size());

            session.flush();

            Thread.sleep(1500);
        }

        String commentString = JSONValue.toJSONString(comments);
        
        PrintWriter out = new PrintWriter("unifiedremote.txt");
        
        System.out.println(commentString);
        
        out.println(JSONValue.toJSONString(comments));
    }
}
