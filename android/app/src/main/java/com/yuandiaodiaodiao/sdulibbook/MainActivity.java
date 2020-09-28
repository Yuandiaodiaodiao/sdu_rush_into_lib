package com.yuandiaodiaodiao.sdulibbook;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        WebView wv=(WebView)findViewById(R.id.webView);
//        wv.setWebChromeClient(new WebChromeClient());

        wv.setWebViewClient(new WebViewClient());

        wv.getSettings().setJavaScriptEnabled(true);
        wv.getSettings().setUseWideViewPort(true);// 设置可以支持缩放
        wv.getSettings().setLoadWithOverviewMode(true);
        wv.getSettings().setBuiltInZoomControls(true);
        wv.getSettings().setSupportZoom(true);
//        webSettings.setTextZoom(75);
        wv.getSettings().setLayoutAlgorithm(WebSettings.LayoutAlgorithm.SINGLE_COLUMN);

        wv.loadUrl("http://sdulib.yuandiaodiaodiao.cn:10279/");
//        wv.loadUrl("http://www.baidu.com");

    }

}
