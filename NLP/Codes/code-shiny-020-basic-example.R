## This script shows how to create a simple web app using Shiny in
## R. It draws a histogram of the eruptions of the Old Faithful
## Geyser. There is a slider in the app where you can modify the
## number of bins in the histogram. Each time you change the number of
## bins, the histogram is redrawn.

## If you haven't installed Shiny yet, you can install it by typing
## `install.packages('shiny')`.
library(shiny)

## Define the user interface (UI) for the app that draws a histogram.
ui <- fluidPage(
    titlePanel("We love NLP!"),         # App title.
    sidebarLayout( # Sidebar layout with input and output definitions.
        sidebarPanel(          # Sidebar panel for inputs.
            sliderInput(       # Input: Slider for the number of bins.
                inputId = "bins",
                label = "Number of bins:",
                min = 1,
                max = 50,
                value = 30)),
        mainPanel(                # Main panel for displaying outputs.
            plotOutput(outputId = "distPlot")))) # Output: Histogram.

## Define server logic required to draw a histogram.
server <- function(input, output) {
    ## We wrap it in a call to `renderPlot` to indicate that (a) it is
    ## reactive and thus should be re-executed when inputs
    ## (i.e. `input$bins` in this case) change, and (b) that its
    ## output is a plot (a histogram in this case).
    output$distPlot <-
        renderPlot({
            x <- faithful$waiting   # Waiting times between eruptions.
            bins <-           # Sequence from min to max waiting time.
                seq(
                    min(x),
                    max(x),
                    length.out = input$bins + 1) # <=== reactive input!
            hist(                   # Draw histogram of waiting times.
                x,
                breaks = bins,
                col = "#75AADB",
                border = "white",
                xlab = "Waiting time to next eruption (in mins)",
                main = "Histogram of waiting times")})}

## Run the Shiny app. You can terminate it by hitting Control-C in the
## R terminal.
shinyApp(ui = ui, server = server)
