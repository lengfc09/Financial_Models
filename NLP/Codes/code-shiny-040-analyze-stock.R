## This script runs a simply Shiny app in R that lets you enter a
## stock symbol and will then grab an up-to-date chart from
## StockCharts.com and display it in your browser.

library('shiny')                        # Load the Shiny R package.

## Define the user interface (UI).
ui <- 
    pageWithSidebar(
        headerPanel("What's the stock market up to?"),
        sidebarPanel(
            textInput(
                inputId = 'ticker',
                label =
                    paste0(
                        'Enter ticker here (e.g. SPY, GOOGL, AAPL). ',
                        'No need to confirm with enter key.'),
                value = 'SPY')),
        mainPanel(
            imageOutput('stockchart')))

## Define the server functionality.
server <- function(input, output) {
    output$stockchart <-
        renderImage({       # Will delete file after usage by default.
            outfile <- tempfile(fileext = '.png') # Temporary file name.
            download.file(      # Download chart from StockCharts.com.
                paste0(
                    'http://stockcharts.com/c-sc/sc?s=',
                    input$ticker,
                    '&p=D&yr=0&mn=4&dy=0&i=p67769731128&r=1516847702061'),
                outfile)
            list(  # Tell `renderImage` how to display the image file.
                src = outfile,
                contentType = 'image/png',
                ## width = 500,
                ## height = 300,
                alt = 'Picture showing stock chart.')})}

## Run the app. You can terminate it by hitting Control-C in the R
## terminal.
shinyApp(ui, server)
