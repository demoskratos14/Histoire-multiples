package com.aventure.desdice

import android.annotation.SuppressLint
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/**
 * Toute l'application vit ici : au lancement, on demarre le serveur Flask
 * existant (dice_web.py) dans un thread Python en arriere-plan, puis on
 * charge son adresse locale dans une WebView integree a l'appli.
 *
 * Resultat pour l'utilisateur : un seul icone a toucher, aucune page de
 * navigateur externe a ouvrir, aucune adresse a taper.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val handler = Handler(Looper.getMainLooper())
    // Doit correspondre exactement a PORT dans android_bridge.py. Different
    // de la version d'origine (5001) expres : 127.0.0.1 est partage par tout
    // l'appareil Android, donc deux apps sur le meme port se genent l'une
    // l'autre si elles tournent toutes les deux en arriere-plan en meme temps.
    private val serverUrl = "http://127.0.0.1:5011"
    private var attempts = 0
    private val maxAttempts = 40 // ~20 secondes de tentatives au premier lancage

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        Python.getInstance()
            .getModule("android_bridge")
            .callAttr("start_server")

        webView = findViewById(R.id.webview)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.webViewClient = object : WebViewClient() {
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame != false) {
                    retryLoad()
                }
            }
        }

        // Petit delai pour laisser le temps au serveur Flask de demarrer
        // dans son thread avant la premiere tentative de chargement.
        handler.postDelayed({ webView.loadUrl(serverUrl) }, 500)
    }

    private fun retryLoad() {
        attempts++
        if (attempts <= maxAttempts) {
            handler.postDelayed({ webView.loadUrl(serverUrl) }, 500)
        }
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
