

// ONLY MAJOR DIFFERENCE is this section
devServer: {
    contentBase: path.join(__dirname, '<JS PATH>')
    publicPath: '/dist/', 
    watchContentBase: true, 
    disableHostCheck: true, 
    host: '0.0.0.0', 
    port: 5000, 
    proxy: { 
        '!(/dist/**.*)': {
            target: 'http://127.0.0.1:5555'
        }
    }, 
    mode: 'development'
}