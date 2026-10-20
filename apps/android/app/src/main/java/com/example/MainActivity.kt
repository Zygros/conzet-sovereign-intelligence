package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountTree
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.MonitorHeart
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.Terminal
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.MonitorHeart
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material.icons.outlined.Terminal
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.components.SovereignTopBar
import com.example.ui.screens.CodexScreen
import com.example.ui.screens.CouncilScreen
import com.example.ui.screens.DashboardScreen
import com.example.ui.screens.ProtocolsScreen
import com.example.ui.screens.SourceMeshScreen
import com.example.ui.theme.BackgroundDark
import com.example.ui.theme.OutlineDark
import com.example.ui.theme.QuantumCyan
import com.example.ui.theme.SovereignCodexTheme
import com.example.ui.theme.SovereignGold
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.TextPrimaryDark
import com.example.ui.theme.TextTertiaryDark
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.NavTab

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            SovereignCodexTheme(darkTheme = true) {
                val viewModel: MainViewModel = viewModel()
                val currentTab by viewModel.currentTab.collectAsState()
                val systemState by viewModel.systemState.collectAsState()

                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    containerColor = BackgroundDark,
                    topBar = {
                        SovereignTopBar(
                            systemState = systemState,
                            onTriggerPulse = { viewModel.triggerPulse() },
                            onResolveFriction = { viewModel.resolveFriction() }
                        )
                    },
                    bottomBar = {
                        SovereignBottomBar(
                            currentTab = currentTab,
                            onSelectTab = { viewModel.setTab(it) }
                        )
                    }
                ) { innerPadding ->
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(innerPadding)
                    ) {
                        AnimatedContent(
                            targetState = currentTab,
                            transitionSpec = {
                                fadeIn() togetherWith fadeOut()
                            },
                            label = "tab_transition"
                        ) { tab ->
                            when (tab) {
                                NavTab.DASHBOARD -> DashboardScreen(viewModel = viewModel)
                                NavTab.CODEX -> CodexScreen(viewModel = viewModel)
                                NavTab.PROTOCOLS -> ProtocolsScreen(viewModel = viewModel)
                                NavTab.MESH -> SourceMeshScreen(viewModel = viewModel)
                                NavTab.COUNCIL -> CouncilScreen(viewModel = viewModel)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun SovereignBottomBar(
    currentTab: NavTab,
    onSelectTab: (NavTab) -> Unit,
    modifier: Modifier = Modifier
) {
    NavigationBar(
        modifier = modifier
            .background(SurfaceDark)
            .windowInsetsPadding(WindowInsets.navigationBars)
            .testTag("sovereign_bottom_bar"),
        containerColor = SurfaceDark,
        tonalElevation = 8.dp
    ) {
        NavTab.values().forEach { tab ->
            val isSelected = currentTab == tab
            val icon = when (tab) {
                NavTab.DASHBOARD -> if (isSelected) Icons.Filled.MonitorHeart else Icons.Outlined.MonitorHeart
                NavTab.CODEX -> if (isSelected) Icons.Filled.AutoAwesome else Icons.Outlined.AutoAwesome
                NavTab.PROTOCOLS -> if (isSelected) Icons.Filled.Terminal else Icons.Outlined.Terminal
                NavTab.MESH -> if (isSelected) Icons.Filled.AccountTree else Icons.Outlined.AccountTree
                NavTab.COUNCIL -> if (isSelected) Icons.Filled.Psychology else Icons.Outlined.Psychology
            }

            NavigationBarItem(
                selected = isSelected,
                onClick = { onSelectTab(tab) },
                icon = {
                    Icon(
                        imageVector = icon,
                        contentDescription = tab.title,
                        modifier = Modifier.size(20.dp)
                    )
                },
                label = {
                    Text(
                        text = tab.title,
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                            fontSize = 10.sp
                        )
                    )
                },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = Color.Black,
                    selectedTextColor = SovereignGold,
                    indicatorColor = SovereignGold,
                    unselectedIconColor = TextTertiaryDark,
                    unselectedTextColor = TextTertiaryDark
                ),
                modifier = Modifier.testTag("nav_tab_${tab.name.lowercase()}")
            )
        }
    }
}
