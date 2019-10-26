package main

import (
	"fmt"
    "os"
    "net/http"
    "time"
    "log"

	"gocv.io/x/gocv"
    //"github.com/google/uuid"
)

const (
    ID = "0"
    API = "https://swagv1.azurewebsites.net/api/analyzeImage"
    TEMP = "./.temp-capture.jpg"
)

func main() {
	dev, err := gocv.OpenVideoCapture(ID)
	if err != nil {
		fmt.Printf("Could not open camera device %v: %v\n", ID, err.Error())
		return
	}
	defer dev.Close()

	img := gocv.NewMat()
	defer img.Close()

    //uuid := uuid.New().String()
    uuid := "1"  // TODO: Un-hard-code
    println(uuid)

    // Continuously beam up images
    for {
        time.Sleep(3100 * time.Millisecond) // Fine as camera needs time to warm up
        if success := dev.Read(&img); !success {
            log.Printf("No data read from camera device %v\n", ID)
            continue
        }
        if img.Empty() {
            log.Printf("No image found on camera device %v\n", ID)
            continue
        }

        // Write image to disk
        // NOTE: gocv currently only supports writing to file. So re-read it and beam it up.
        if success := gocv.IMWrite(TEMP, img); !success {
            continue
        }
        file, err := os.Open(TEMP)
        if err != nil {
            fmt.Printf("Could not re-read image file: %v\n", err.Error())
            continue
        }

        // TODO: If problematic, switch to image/jpg
        // POST image
        resp, err := http.Post(API + "?" + "pid=" + uuid, "application/octet-stream", file)
        if err != nil {
            log.Printf("Could not POST image file successfully: %v \n -> \n %v \n", err.Error(), resp)
            continue
        } else if resp.StatusCode != 200 {
            log.Printf("Could not POST image file successfully: %v \n -> \n %v \n", resp.StatusCode, resp)
            continue
        } else {
            log.Printf("Image sent successfully\n")
        }
    }
}
