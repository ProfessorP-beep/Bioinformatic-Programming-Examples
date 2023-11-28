#Load library to source python within R script
library(reticulate)
library(keras)
library(tensorflow)
library(shiny)

#load model
model_load <- load_model_tf('tensorflow/cnn-mnist/')

# Define the UI
ui <- fluidPage(
  # App title ----
  titlePanel("Hello TensorFlow!"),
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    # Sidebar panel for inputs ----
    sidebarPanel(
      # Input: File upload
      fileInput("image_path", label = "Input a JPEG image")
    ),
    # Main panel for displaying outputs ----
    mainPanel(
      # Output: Histogram ----
      textOutput(outputId = "prediction"),
      plotOutput(outputId = "image")
    )
  )
)

# Define server logic required to draw a histogram ----
server <- function(input, output) {
  
  image <- reactive({
    req(input$image_path)
    jpeg::readJPEG(input$image_path$datapath)
  })
  
  output$prediction <- renderText({
    
    img <- image() %>% 
      array_reshape(., dim = c(1, dim(.), 1))
    #predict_classes is deprecated. Since this is a multi-class classification we use the model_load predict pipe below
    paste0("The predicted class number is ", model_load %>% predict(img) %>% k_argmax())
  })
  
  output$image <- renderPlot({
    plot(as.raster(image()))
  })
  
}

shinyApp(ui, server)