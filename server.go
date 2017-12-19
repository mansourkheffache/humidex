/*

// check errors returned at various points in the code... panic if something happens...
func check(e error) {
    if e != nil {
        panic(e)
    }
}



func mainPageHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	fmt.Printf("Request arrived to URL: %s\n\n", r.URL)
	dat, err := ioutil.ReadFile("./index.htm")
	check(err)
	fmt.Fprintf(w,string(dat))
}

func main() {
           
              http.HandleFunc("/", mainPageHandler)
              http.ListenAndServe(":8080", nil)
}   */


package main

import (
  "log"
  "net/http"
)

func main() {
  fs := http.FileServer(http.Dir("html"))
  http.Handle("/", fs)
  log.Println("Listening...")
  http.ListenAndServe(":8080", nil)
}