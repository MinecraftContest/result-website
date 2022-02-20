const webpack = require('webpack')
const path = require('path')
const CopyPlugin = require('copy-webpack-plugin')

const config = {
  mode: 'development',
  entry: path.resolve(__dirname, './viewer.js'),
  output: {
    path: path.resolve(__dirname, './public'),
    filename: './viewer.js'
  },
  resolve: {
    fallback: {
      zlib: require.resolve('browserify-zlib'),
      stream: require.resolve('stream-browserify'),
      buffer: require.resolve('buffer/'),
      events: require.resolve('events/'),
      assert: require.resolve('assert/')
    }
  },
  plugins: [
    // fix "process is not defined" error:
    new webpack.ProvidePlugin({
      process: 'process/browser'
    }),
    new webpack.ProvidePlugin({
      Buffer: ['buffer', 'Buffer']
    }),
    new webpack.NormalModuleReplacementPlugin(
      /prismarine-viewer[/|\\]viewer[/|\\]lib[/|\\]utils/,
      './utils.web.js'
    ),
    new CopyPlugin({
      patterns: [
        { from: 'prismarine-viewer/public/blocksStates/', to: './blocksStates/' },
        { from: 'prismarine-viewer/public/textures/', to: './textures/' },
        { from: 'prismarine-viewer/public/worker.js', to: './' },
        { from: 'prismarine-viewer/public/supportedVersions.json', to: './' }
      ]
    })
  ],
  devServer: {
    contentBase: path.resolve(__dirname, './public'),
    compress: true,
    inline: true,
    // open: true,
    hot: true,
    watchOptions: {
      ignored: /node_modules/
    }
  }
}

module.exports = config
