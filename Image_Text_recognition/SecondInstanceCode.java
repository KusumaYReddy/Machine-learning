package second_instance;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Scanner;
import java.util.Map.Entry;

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.services.rekognition.model.AmazonRekognitionException;
import com.amazonaws.services.rekognition.model.DetectLabelsRequest;
import com.amazonaws.services.rekognition.model.DetectLabelsResult;
import com.amazonaws.services.rekognition.model.DetectTextRequest;
import com.amazonaws.services.rekognition.model.DetectTextResult;
import com.amazonaws.services.rekognition.model.Image;
import com.amazonaws.services.rekognition.model.Label;
import com.amazonaws.services.rekognition.model.S3Object;
import com.amazonaws.services.rekognition.model.TextDetection;
import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import com.amazonaws.services.sqs.model.CreateQueueRequest;
import com.amazonaws.services.sqs.model.DeleteMessageRequest;
import com.amazonaws.services.sqs.model.DeleteQueueRequest;
import com.amazonaws.services.sqs.model.Message;
import com.amazonaws.services.sqs.model.ReceiveMessageRequest;
import com.amazonaws.services.sqs.model.SendMessageRequest;

public class ec2   {
	public static void main(String[] args) {
	AmazonSQS sqs = AmazonSQSClientBuilder.standard()
            .withRegion(Regions.US_EAST_1)
            .build();
	 
	AmazonRekognition rekognitionClient = AmazonRekognitionClientBuilder.standard().build();

    String QueueUrl="paste your queue url";
    String bucket = "njit-cs-643";
   ReceiveMessageRequest receiveMessageRequest = new ReceiveMessageRequest(QueueUrl);
   receiveMessageRequest.withMaxNumberOfMessages(10);
   
   List<Message> messages = sqs.receiveMessage(receiveMessageRequest).getMessages();
   StringBuffer s=new StringBuffer();
   while (messages.size() > 0) {
    for (Message message : messages) {
        DetectTextRequest request = new DetectTextRequest()
                .withImage(new Image()
                .withS3Object(new S3Object()
                .withName(message.getBody()).withBucket(bucket)));
    	try {

            DetectTextResult result = rekognitionClient.detectText(request);
            List<TextDetection> textDetections = result.getTextDetections();
            if(textDetections.size()>0) {
            s.append("Detected lines and words for " + message.getBody());
            s.append(System.lineSeparator());
            s.append(textDetections.get(0).getDetectedText());
            s.append(System.lineSeparator());
            System.out.println("lines:::"+s);
         
			
            
            try {
                File myObj = new File("textoutput.txt");
                if (myObj.createNewFile()) {
                  System.out.println("File created: " + myObj.getName());
                } else {
                  System.out.println("File already exists.");
                 }
              } catch (IOException e) {
                System.out.println("An error occurred.");
                e.printStackTrace();
              }
            
            try {
                FileWriter myWriter = new FileWriter("textoutput.txt");
                myWriter.write(s.toString());
                System.out.println("Successfully wrote to the file.");
               myWriter.close();
            }
               catch (IOException e) {
                System.out.println("An error occurred.");
                e.printStackTrace();
              }            
    }
    	}

    catch (AmazonRekognitionException e) {
        e.printStackTrace();
    }
}
    receiveMessageRequest = new ReceiveMessageRequest(QueueUrl);
    receiveMessageRequest.withMaxNumberOfMessages(10);
    messages = sqs.receiveMessage(receiveMessageRequest).getMessages();
}
  
    }
	}

	
