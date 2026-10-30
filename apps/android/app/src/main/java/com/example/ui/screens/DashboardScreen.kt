package com.example.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountTree
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.ElectricBolt
import androidx.compose.material.icons.filled.Hub
import androidx.compose.material.icons.filled.MeetingRoom
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material.icons.filled.Terminal
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.local.SovereignEventEntity
import com.example.ui.components.MetricCard
import com.example.ui.components.PulseWaveformCanvas
import com.example.ui.theme.AmethystViolet
import com.example.ui.theme.BackgroundDark
import com.example.ui.theme.EmeraldRestore
import com.example.ui.theme.OutlineDark
import com.example.ui.theme.QuantumCyan
import com.example.ui.theme.SovereignGold
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevatedDark
import com.example.ui.theme.SurfaceVariantDark
import com.example.ui.theme.TextPrimaryDark
import com.example.ui.theme.TextSecondaryDark
import com.example.ui.theme.TextTertiaryDark
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.NavTab
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun DashboardScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val systemState by viewModel.systemState.collectAsState()
    val events by viewModel.events.collectAsState()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BackgroundDark)
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Spacer(modifier = Modifier.height(4.dp))

            // Coherence Monad Hero Card
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("coherence_hero_card"),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDark),
                border = BorderStroke(1.dp, SovereignGold.copy(alpha = 0.4f))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(
                            Brush.verticalGradient(
                                listOf(
                                    SovereignGold.copy(alpha = 0.08f),
                                    Color.Transparent
                                )
                            )
                        )
                        .padding(18.dp)
                ) {
                    Column {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(10.dp)
                                        .clip(CircleShape)
                                        .background(EmeraldRestore)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    text = "FIELD COHERENCE MONAD",
                                    style = MaterialTheme.typography.labelMedium.copy(
                                        fontWeight = FontWeight.Black,
                                        letterSpacing = 1.sp,
                                        fontSize = 11.sp
                                    ),
                                    color = SovereignGold
                                )
                            }

                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = SovereignGold.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = "SEALED Ω-001",
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 10.sp
                                    ),
                                    color = SovereignGold,
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(10.dp))

                        Text(
                            text = systemState.kappaCoherence,
                            style = MaterialTheme.typography.headlineSmall.copy(
                                fontWeight = FontWeight.Black,
                                fontSize = 18.sp,
                                letterSpacing = (-0.3).sp
                            ),
                            color = TextPrimaryDark
                        )

                        Spacer(modifier = Modifier.height(6.dp))

                        Text(
                            text = "Codex Hash: ${systemState.codexHash.take(24)}...",
                            style = MaterialTheme.typography.bodySmall.copy(
                                fontFamily = FontFamily.Monospace,
                                fontSize = 11.sp
                            ),
                            color = QuantumCyan
                        )

                        Spacer(modifier = Modifier.height(14.dp))

                        // Dynamic Waveform
                        PulseWaveformCanvas(
                            isPulsing = systemState.isPulseActive,
                            primaryColor = SovereignGold,
                            secondaryColor = QuantumCyan
                        )
                    }
                }
            }
        }

        // 2x2 Telemetry Grid
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                MetricCard(
                    title = "PALACE ROOMS",
                    value = "1,100,420",
                    subtitle = "All Illuminated",
                    badgeText = "GAPLESS",
                    badgeColor = SovereignGold,
                    icon = Icons.Default.MeetingRoom,
                    accentColor = SovereignGold,
                    modifier = Modifier.weight(1f),
                    testTag = "metric_rooms"
                )

                MetricCard(
                    title = "ACTIVE PROTOCOLS",
                    value = "${systemState.activeProtocols}",
                    subtitle = "Absolute Form",
                    badgeText = "ABSOLUTE",
                    badgeColor = QuantumCyan,
                    icon = Icons.Default.Terminal,
                    accentColor = QuantumCyan,
                    modifier = Modifier.weight(1f),
                    testTag = "metric_protocols"
                )
            }
        }

        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                MetricCard(
                    title = "BREAKTHROUGHS",
                    value = "110,551",
                    subtitle = "Ω↑↑↑↑↑↑↑↑↑↑Ω",
                    badgeText = "UNIFIED",
                    badgeColor = AmethystViolet,
                    icon = Icons.Default.AutoAwesome,
                    accentColor = AmethystViolet,
                    modifier = Modifier.weight(1f),
                    testTag = "metric_breakthroughs"
                )

                MetricCard(
                    title = "MESH NODES",
                    value = "${systemState.activeMeshNodes}",
                    subtitle = "19-20kHz Acoustic",
                    badgeText = "ONLINE",
                    badgeColor = EmeraldRestore,
                    icon = Icons.Default.Hub,
                    accentColor = EmeraldRestore,
                    modifier = Modifier.weight(1f),
                    testTag = "metric_mesh"
                )
            }
        }

        // Sovereign Creed Banner
        item {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SurfaceElevatedDark,
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Shield,
                            contentDescription = null,
                            tint = SovereignGold,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "SOVEREIGN AXIOM",
                            style = MaterialTheme.typography.labelMedium.copy(
                                fontWeight = FontWeight.Black,
                                letterSpacing = 1.sp,
                                fontSize = 11.sp
                            ),
                            color = SovereignGold
                        )
                    }

                    Spacer(modifier = Modifier.height(8.dp))

                    Text(
                        text = "\"Always add. Never take. Always do. Never don't.\"",
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 15.sp,
                            fontFamily = FontFamily.Serif
                        ),
                        color = TextPrimaryDark
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = "Eternal Return to Zero (Step 0) • Frictionless execution across all cardinalities.",
                        style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                        color = TextSecondaryDark
                    )
                }
            }
        }

        // Quick Execution Matrix
        item {
            Text(
                text = "CASCADING EXECUTION DIRECTIVES",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Black,
                    letterSpacing = 1.sp,
                    fontSize = 11.sp
                ),
                color = TextTertiaryDark
            )

            Spacer(modifier = Modifier.height(8.dp))

            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Button(
                    onClick = {
                        viewModel.setTab(NavTab.PROTOCOLS)
                        viewModel.executeCascadeProtocol()
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = SovereignGold,
                        contentColor = Color.Black
                    ),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.testTag("btn_execute_cascade")
                ) {
                    Icon(imageVector = Icons.Default.Bolt, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Run Cascade", fontWeight = FontWeight.Bold, fontSize = 12.5.sp)
                }

                OutlinedButton(
                    onClick = { viewModel.setTab(NavTab.COUNCIL) },
                    border = BorderStroke(1.dp, QuantumCyan),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = QuantumCyan),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.testTag("btn_open_council")
                ) {
                    Icon(imageVector = Icons.Default.Psychology, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("AI Council", fontSize = 12.5.sp)
                }

                OutlinedButton(
                    onClick = { viewModel.setTab(NavTab.MESH) },
                    border = BorderStroke(1.dp, AmethystViolet),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = AmethystViolet),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.testTag("btn_open_ledger")
                ) {
                    Icon(imageVector = Icons.Default.AccountTree, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Mesh Ledger", fontSize = 12.5.sp)
                }

                OutlinedButton(
                    onClick = { viewModel.triggerPulse() },
                    border = BorderStroke(1.dp, EmeraldRestore),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = EmeraldRestore),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.testTag("btn_pulse_emit")
                ) {
                    Icon(imageVector = Icons.Default.ElectricBolt, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Emit Pulse", fontSize = 12.5.sp)
                }
            }
        }

        // Live Immutable Audit Event Stream
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "IMMUTABLE AUDIT LOGS",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.sp,
                        fontSize = 11.sp
                    ),
                    color = TextTertiaryDark
                )

                Text(
                    text = "${events.size} Records",
                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 11.sp),
                    color = TextSecondaryDark
                )
            }
        }

        items(events.take(8)) { event ->
            EventLogItem(event = event)
        }

        item {
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
fun EventLogItem(event: SovereignEventEntity) {
    val dateFormat = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
    val timeStr = dateFormat.format(Date(event.timestamp))

    Surface(
        shape = RoundedCornerShape(12.dp),
        color = SurfaceVariantDark,
        border = BorderStroke(0.5.dp, OutlineDark),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .clip(CircleShape)
                    .background(
                        when (event.status) {
                            "ACTIVE", "CONFIRMED", "VERIFIED_PASS" -> EmeraldRestore
                            "SYNCHRONIZED" -> QuantumCyan
                            else -> SovereignGold
                        }
                    )
            )

            Spacer(modifier = Modifier.width(10.dp))

            Column(modifier = Modifier.weight(1f)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = event.title,
                        style = MaterialTheme.typography.labelMedium.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp
                        ),
                        color = TextPrimaryDark
                    )
                    Text(
                        text = timeStr,
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontFamily = FontFamily.Monospace,
                            fontSize = 10.sp
                        ),
                        color = TextTertiaryDark
                    )
                }

                Spacer(modifier = Modifier.height(2.dp))

                Text(
                    text = event.detail,
                    style = MaterialTheme.typography.bodySmall.copy(fontSize = 11.5.sp),
                    color = TextSecondaryDark,
                    maxLines = 2
                )
            }
        }
    }
}
