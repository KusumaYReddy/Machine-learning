
package com.amazonaws.samples;

import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.ListObjectsV2Result;
import com.amazonaws.services.s3.model.S3ObjectSummary;
import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import com.amazonaws.services.sqs.model.SendMessageRequest;
import com.amazonaws.services.rekognition.model.BoundingBox;
import com.amazonaws.services.rekognition.model.DetectLabelsRequest;
import com.amazonaws.services.rekognition.model.DetectLabelsResult;
import com.amazonaws.services.rekognition.model.Image;
import com.amazonaws.services.rekognition.model.Instance;
import com.amazonaws.services.rekognition.model.Label;
import com.amazonaws.services.rekognition.model.Parent;
import com.amazonaws.services.rekognition.model.S3Object;
import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.services.rekognition.model.AmazonRekognitionException;

import java.io.FileInputStream;
import java.util.Date;
import java.util.List;
import java.util.Properties;

public class S3Sample {
    public static void main(String[] args) {
        
        String bucket = "njit-cs-643";
        String QueueUrl="paste your queue url";
       
        
        final AmazonS3 s3 = AmazonS3ClientBuilder.standard().withRegion(Regions.US_EAST_1).build();
        ListObjectsV2Result result = s3.listObjectsV2(bucket);
        List<S3ObjectSummary> objects = result.getObjectSummaries();
        for (S3ObjectSummary os : objects) {
        String photo =os.getKey().toString();
        AmazonRekognition rekognitionClient = AmazonRekognitionClientBuilder.standard().build();

        DetectLabelsRequest request = new DetectLabelsRequest()
                .withImage(new Image().withS3Object(new S3Object().withName(photo).withBucket(bucket)))
                .withMaxLabels(10).withMinConfidence(75F);
        AmazonSQS sqs = AmazonSQSClientBuilder.standard()
                .withRegion(Regions.US_EAST_1)
                .build();
       
        
 
        
        try {
            DetectLabelsResult result1 = rekognitionClient.detectLabels(request);
            List<Label> labels = result1.getLabels();

            for (Label label : labels) {
                if(label.getName().compareTo("Car")==0 && label.getConfidence()>90) {
                	System.out.println(os.getKey());
                	sqs.sendMessage(new SendMessageRequest(QueueUrl, os.getKey()));
                }
            }
        }
        catch (AmazonRekognitionException e) {
            e.printStackTrace();
        }
    }
    }
}
