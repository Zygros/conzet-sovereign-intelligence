package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.HourglassTop
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material.icons.filled.Speed
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.FaultSimulationResult
import com.example.data.model.ProtocolState
import com.example.data.model.ProtocolStep
import com.example.ui.theme.BackgroundDark
import com.example.ui.theme.CrimsonFriction
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

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ProtocolsScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val steps by viewModel.protocolSteps.collectAsState()
    val isExecuting by viewModel.isProtocolExecuting.collectAsState()
    val faultResult by viewModel.lastFaultResult.collectAsState()
    val pastRuns by viewModel.protocolRuns.collectAsState()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BackgroundDark)
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Spacer(modifier = Modifier.height(4.dp))

            // Header banner
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDark),
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = "HACPP-1.0 PROTOCOL ENGINE",
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.Black,
                                    letterSpacing = 1.sp,
                                    fontSize = 16.sp
                                ),
                                color = SovereignGold
                            )
                            Text(
                                text = "8-Phase Cascading Verification & Invariant Handshake",
                                style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                                color = TextSecondaryDark
                            )
                        }

                        Button(
                            onClick = { viewModel.executeCascadeProtocol() },
                            enabled = !isExecuting,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = SovereignGold,
                                contentColor = Color.Black
                            ),
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.testTag("run_cascade_button")
                        ) {
                            if (isExecuting) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(16.dp),
                                    strokeWidth = 2.dp,
                                    color = Color.Black
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("Running...", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            } else {
                                Icon(
                                    imageVector = Icons.Default.PlayArrow,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Execute", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }

        // Stepper: 8 Phases
        item {
            Text(
                text = "WORKFLOW CASCADE PIPELINE",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Black,
                    letterSpacing = 1.sp,
                    fontSize = 11.sp
                ),
                color = TextTertiaryDark
            )

            Spacer(modifier = Modifier.height(8.dp))

            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SurfaceVariantDark,
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    steps.forEachIndexed { index, step ->
                        ProtocolStepRow(step = step, isLast = index == steps.size - 1)
                    }
                }
            }
        }

        // Fault Injection & BTO Testing Matrix (F1-F7)
        item {
            Text(
                text = "BOUNDED RECOVERY-TIME (BTO) FAULT INJECTOR",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Black,
                    letterSpacing = 1.sp,
                    fontSize = 11.sp
                ),
                color = TextTertiaryDark
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = "Inject physical & software faults to verify bounded restoration SLOs without zero-latency deception.",
                style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                color = TextSecondaryDark
            )

            Spacer(modifier = Modifier.height(10.dp))

            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                val faults = listOf(
                    "F1" to "Transient Link Fault",
                    "F2" to "Compute Tile Fault",
                    "F3" to "Memory ECC Burst",
                    "F4" to "Controller Loss",
                    "F5" to "Software Crash",
                    "F6" to "Correlated Outage",
                    "F7" to "Integrity Refusal"
                )

                faults.forEach { (code, name) ->
                    OutlinedButton(
                        onClick = { viewModel.injectFaultSimulation(code, name) },
                        shape = RoundedCornerShape(10.dp),
                        border = BorderStroke(1.dp, OutlineDark),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = TextPrimaryDark),
                        modifier = Modifier.testTag("fault_btn_$code")
                    ) {
                        Surface(
                            shape = RoundedCornerShape(4.dp),
                            color = when (code) {
                                "F1", "F2" -> QuantumCyan.copy(alpha = 0.2f)
                                "F3", "F4" -> SovereignGold.copy(alpha = 0.2f)
                                "F5", "F6" -> CrimsonFriction.copy(alpha = 0.2f)
                                else -> EmeraldRestore.copy(alpha = 0.2f)
                            }
                        ) {
                            Text(
                                text = code,
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Black,
                                    fontSize = 10.sp
                                ),
                                color = TextPrimaryDark,
                                modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(name, fontSize = 11.5.sp)
                    }
                }
            }
        }

        // Display Last Fault Result if present
        faultResult?.let { result ->
            item {
                FaultResultCard(result = result)
            }
        }

        // Protocol Runs History
        if (pastRuns.isNotEmpty()) {
            item {
                Text(
                    text = "VERIFIED EXECUTION RUNS",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.sp,
                        fontSize = 11.sp
                    ),
                    color = TextTertiaryDark
                )
            }

            items(pastRuns.take(5)) { run ->
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
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = run.protocolName,
                                style = MaterialTheme.typography.labelMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 13.sp
                                ),
                                color = TextPrimaryDark
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = "${run.testId} • ${run.totalTimeMs}ms • Hash: ${run.auditHash.take(12)}...",
                                style = MaterialTheme.typography.bodySmall.copy(
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 10.5.sp
                                ),
                                color = TextSecondaryDark
                            )
                        }

                        Surface(
                            shape = RoundedCornerShape(6.dp),
                            color = EmeraldRestore.copy(alpha = 0.2f)
                        ) {
                            Text(
                                text = if (run.passed) "PASS" else "DEGRADED",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 10.sp
                                ),
                                color = EmeraldRestore,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                }
            }
        }

        item {
            Spacer(modifier = Modifier.height(20.dp))
        }
    }
}

@Composable
fun ProtocolStepRow(step: ProtocolStep, isLast: Boolean) {
    val stateColor = when (step.status) {
        ProtocolState.CLOSED, ProtocolState.VERIFIED -> EmeraldRestore
        ProtocolState.EXECUTING -> SovereignGold
        ProtocolState.IDLE -> TextTertiaryDark
        else -> QuantumCyan
    }

    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.Top
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Box(
                modifier = Modifier
                    .size(24.dp)
                    .clip(CircleShape)
                    .background(stateColor.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                if (step.status == ProtocolState.CLOSED || step.status == ProtocolState.VERIFIED) {
                    Icon(
                        imageVector = Icons.Default.Check,
                        contentDescription = null,
                        tint = EmeraldRestore,
                        modifier = Modifier.size(14.dp)
                    )
                } else if (step.status == ProtocolState.EXECUTING) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(14.dp),
                        strokeWidth = 2.dp,
                        color = SovereignGold
                    )
                } else {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(TextTertiaryDark)
                    )
                }
            }

            if (!isLast) {
                Box(
                    modifier = Modifier
                        .width(2.dp)
                        .height(30.dp)
                        .background(OutlineDark)
                )
            }
        }

        Spacer(modifier = Modifier.width(12.dp))

        Column(
            modifier = Modifier
                .weight(1f)
                .padding(bottom = if (isLast) 0.dp else 12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = step.name,
                    style = MaterialTheme.typography.labelMedium.copy(
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp
                    ),
                    color = if (step.status != ProtocolState.IDLE) TextPrimaryDark else TextSecondaryDark
                )

                if (step.executionMs > 0) {
                    Text(
                        text = "${step.executionMs}ms",
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontFamily = FontFamily.Monospace,
                            fontSize = 10.sp
                        ),
                        color = SovereignGold
                    )
                }
            }

            Text(
                text = step.description,
                style = MaterialTheme.typography.bodySmall.copy(fontSize = 11.5.sp),
                color = TextSecondaryDark
            )
        }
    }
}

@Composable
fun FaultResultCard(result: FaultSimulationResult) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = SurfaceElevatedDark,
        border = BorderStroke(1.dp, EmeraldRestore.copy(alpha = 0.5f)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.CheckCircle,
                        contentDescription = null,
                        tint = EmeraldRestore,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "TEST ${result.testId} PASSED",
                        style = MaterialTheme.typography.labelMedium.copy(
                            fontWeight = FontWeight.Black,
                            letterSpacing = 1.sp,
                            fontSize = 12.sp
                        ),
                        color = EmeraldRestore
                    )
                }

                Surface(
                    shape = RoundedCornerShape(6.dp),
                    color = EmeraldRestore.copy(alpha = 0.2f)
                ) {
                    Text(
                        text = result.serviceMode,
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 10.sp
                        ),
                        color = EmeraldRestore,
                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = "${result.faultName} (${result.faultClass})",
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp
                ),
                color = TextPrimaryDark
            )

            Spacer(modifier = Modifier.height(12.dp))

            // Timing metrics breakdown
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                TimeStat(label = "Td (Detect)", value = "${result.detectionMs}ms")
                TimeStat(label = "Tc (Contain)", value = "${result.containmentMs}ms")
                TimeStat(label = "Tr (Recover)", value = "${result.recoveryMs}ms")
                TimeStat(label = "Tv (Verify)", value = "${result.verificationMs}ms")
                TimeStat(label = "Ttotal", value = "${result.totalRestorationMs}ms", highlight = true)
            }

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = "Audit Hash: ${result.auditHash}",
                style = MaterialTheme.typography.bodySmall.copy(
                    fontFamily = FontFamily.Monospace,
                    fontSize = 9.5.sp
                ),
                color = QuantumCyan,
                maxLines = 1
            )
        }
    }
}

@Composable
fun TimeStat(label: String, value: String, highlight: Boolean = false) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp),
            color = TextTertiaryDark
        )
        Spacer(modifier = Modifier.height(2.dp))
        Text(
            text = value,
            style = MaterialTheme.typography.labelMedium.copy(
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Bold,
                fontSize = 12.sp
            ),
            color = if (highlight) SovereignGold else TextPrimaryDark
        )
    }
}
