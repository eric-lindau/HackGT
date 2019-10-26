package main

import (
	"fmt"
	"os"
    "time"

	"gocv.io/x/gocv"
)

const ID = "0"

func main() {
	saveFile := os.Args[1]

	dev, err := gocv.OpenVideoCapture(ID)
	if err != nil {
		fmt.Printf("Could not open camera device %v: %v\n", ID, err.Error())
		return
	}
	defer dev.Close()

	img := gocv.NewMat()
	defer img.Close()

    // Camera requires some time to warm up
    time.Sleep(300 * time.Millisecond)
	if success := dev.Read(&img); !success {
		fmt.Printf("No data read from camera device %v\n", ID)
		return
	}
	if img.Empty() {
		fmt.Printf("No image found on camera device %v\n", ID)
		return
	}

	gocv.IMWrite(saveFile, img)
}
