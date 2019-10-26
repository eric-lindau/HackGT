package main

import (
	"fmt"
    "os"
    "net/http"
    "time"

	"gocv.io/x/gocv"
    "github.com/google/uuid"
)

const (
    ID = "0"
    API = ""
    TEMP = ".temp-capture.jpg"
)

func main() {
	dev, err := gocv.OpenVideoCapture(ID)
	if err != nil {
		fmt.Printf("Could not open camera device %v: %v\n", ID, err.Error())
		return
	}
	defer dev.Close()
    // Camera requires some time to warm up
    time.Sleep(300 * time.Millisecond)

	img := gocv.NewMat()
	defer img.Close()

    uuid := uuid.New().String()
    print(uuid)

    // Continuously beam up images
    for {
        if success := dev.Read(&img); !success {
            fmt.Printf("No data read from camera device %v\n", ID)
            return
        }
        if img.Empty() {
            fmt.Printf("No image found on camera device %v\n", ID)
            return
        }

        // Write image to disk
        // NOTE: gocv currently only supports writing to file. So re-read it and beam it up.
        gocv.IMWrite(TEMP, img)
        file, err := os.Open(TEMP)
        if err != nil {
            fmt.Printf("Could not re-read image file: %v\n", err.Error())
            return
        }

        // TODO: If problematic, switch to image/jpg
        // POST image
        resp, err := http.Post(API + "?" + "pid=" + uuid, "application/octet-stream", file)
        if err != nil {
            fmt.Printf("Could not POST image file successfully: %v\n", err.Error())
        } else if resp.StatusCode != 200 {
            fmt.Printf("Could not POST image file successfully: %v\n", resp.StatusCode)
        }

        time.Sleep(3 * time.Second)
    }
}
