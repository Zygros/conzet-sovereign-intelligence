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
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
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
import com.example.data.model.CouncilPerspective
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

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun CouncilScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val prompt by viewModel.councilPrompt.collectAsState()
    val perspectives by viewModel.councilPerspectives.collectAsState()
    val isSynthesizing by viewModel.isCouncilSynthesizing.collectAsState()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(BackgroundDark)
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Spacer(modifier = Modifier.height(4.dp))

            // Header Banner
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDark),
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Text(
                        text = "MULTI-MODEL COUNCIL & BENCHMARK LADDER",
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Black,
                            letterSpacing = 1.sp,
                            fontSize = 15.sp
                        ),
                        color = SovereignGold
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "Synthesizes multi-perspective consensus across Claude, Gemini, GPT-5, and Grok with L0–L5 capability evolution gates.",
                        style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                        color = TextSecondaryDark
                    )
                }
            }
        }

        // Prompt Input & Synthesis trigger
        item {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SurfaceVariantDark,
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "COUNCIL INQUIRY PROMPT",
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp,
                            fontSize = 11.sp
                        ),
                        color = TextTertiaryDark
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    OutlinedTextField(
                        value = prompt,
                        onValueChange = { viewModel.updateCouncilPrompt(it) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .testTag("council_prompt_input"),
                        minLines = 2,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = SurfaceDark,
                            unfocusedContainerColor = SurfaceDark,
                            focusedBorderColor = SovereignGold,
                            unfocusedBorderColor = OutlineDark,
                            focusedTextColor = TextPrimaryDark,
                            unfocusedTextColor = TextPrimaryDark
                        ),
                        shape = RoundedCornerShape(12.dp)
                    )

                    Spacer(modifier = Modifier.height(10.dp))

                    // Preset prompt pills
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        val samples = listOf(
                            "Sanov-Conzet 180T:1 scaling proof",
                            "Acoustic 19-20kHz Gossip vs RF",
                            "Bounded Recovery BTO (F1-F7) matrix"
                        )
                        samples.forEach { sample ->
                            Surface(
                                onClick = {
                                    viewModel.updateCouncilPrompt(sample)
                                    viewModel.runCouncilSynthesis()
                                },
                                shape = RoundedCornerShape(8.dp),
                                color = SurfaceElevatedDark,
                                border = BorderStroke(0.5.dp, OutlineDark)
                            ) {
                                Text(
                                    text = sample,
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                                    color = TextSecondaryDark,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    Button(
                        onClick = { viewModel.runCouncilSynthesis() },
                        enabled = !isSynthesizing,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(44.dp)
                            .testTag("run_synthesis_button"),
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = SovereignGold,
                            contentColor = Color.Black
                        )
                    ) {
                        if (isSynthesizing) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                strokeWidth = 2.dp,
                                color = Color.Black
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Synthesizing Council...", fontSize = 12.5.sp, fontWeight = FontWeight.Bold)
                        } else {
                            Icon(imageVector = Icons.Default.AutoAwesome, contentDescription = null, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Synthesize Multi-Model Consensus", fontSize = 12.5.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }

        // L0-L5 Evolution Ladder Matrix
        item {
            Text(
                text = "CAPABILITY EVOLUTION LADDER (L0 – L5 GATES)",
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
                color = SurfaceElevatedDark,
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    LadderRow(level = "L0", name = "Transfer & Baseline", score = "98%", passed = true)
                    LadderRow(level = "L1", name = "Abstraction & Compression", score = "96%", passed = true)
                    LadderRow(level = "L2", name = "Planning & Decomposition", score = "94%", passed = true)
                    LadderRow(level = "L3", name = "Tool Tree & Sandbox Execution", score = "97%", passed = true)
                    LadderRow(level = "L4", name = "Scientific Reasoning & Proofs", score = "95%", passed = true)
                    LadderRow(level = "L5", name = "Ontological Field Transcendence", score = "100%", passed = true, highlight = true)
                }
            }
        }

        // Council Perspectives
        item {
            Text(
                text = "COUNCIL PERSPECTIVES & CONSENSUS",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Black,
                    letterSpacing = 1.sp,
                    fontSize = 11.sp
                ),
                color = TextTertiaryDark
            )
        }

        items(perspectives) { p ->
            CouncilPerspectiveItem(perspective = p)
        }

        item {
            Spacer(modifier = Modifier.height(20.dp))
        }
    }
}

@Composable
fun LadderRow(
    level: String,
    name: String,
    score: String,
    passed: Boolean,
    highlight: Boolean = false
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Surface(
                shape = RoundedCornerShape(4.dp),
                color = if (highlight) SovereignGold.copy(alpha = 0.2f) else QuantumCyan.copy(alpha = 0.15f)
            ) {
                Text(
                    text = level,
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Black,
                        fontSize = 10.sp
                    ),
                    color = if (highlight) SovereignGold else QuantumCyan,
                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                )
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = name,
                style = MaterialTheme.typography.bodySmall.copy(
                    fontWeight = if (highlight) FontWeight.Bold else FontWeight.Normal,
                    fontSize = 12.sp
                ),
                color = if (highlight) SovereignGold else TextPrimaryDark
            )
        }

        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = score,
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 11.sp
                ),
                color = EmeraldRestore
            )
            Spacer(modifier = Modifier.width(6.dp))
            Icon(
                imageVector = Icons.Default.CheckCircle,
                contentDescription = null,
                tint = EmeraldRestore,
                modifier = Modifier.size(14.dp)
            )
        }
    }
}

@Composable
fun CouncilPerspectiveItem(perspective: CouncilPerspective) {
    val modelColor = when {
        perspective.modelName.contains("Claude", ignoreCase = true) -> SovereignGold
        perspective.modelName.contains("Gemini", ignoreCase = true) -> QuantumCyan
        perspective.modelName.contains("GPT", ignoreCase = true) -> EmeraldRestore
        else -> AmethystViolet
    }

    Surface(
        shape = RoundedCornerShape(16.dp),
        color = SurfaceVariantDark,
        border = BorderStroke(1.dp, OutlineDark),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(modelColor)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = perspective.modelName,
                        style = MaterialTheme.typography.titleSmall.copy(
                            fontWeight = FontWeight.Black,
                            fontSize = 14.sp
                        ),
                        color = TextPrimaryDark
                    )
                }

                Surface(
                    shape = RoundedCornerShape(6.dp),
                    color = modelColor.copy(alpha = 0.15f)
                ) {
                    Text(
                        text = "${(perspective.consensusScore * 100).toInt()}% Consensus",
                        style = MaterialTheme.typography.labelSmall.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 10.sp
                        ),
                        color = modelColor,
                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = perspective.role,
                style = MaterialTheme.typography.labelSmall.copy(fontSize = 11.sp),
                color = modelColor
            )

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = perspective.synthesisText,
                style = MaterialTheme.typography.bodySmall.copy(
                    fontSize = 12.5.sp,
                    lineHeight = 18.sp
                ),
                color = TextPrimaryDark
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Status: ${perspective.uncertaintyFlag}",
                style = MaterialTheme.typography.labelSmall.copy(
                    fontFamily = FontFamily.Monospace,
                    fontSize = 10.sp
                ),
                color = TextTertiaryDark
            )
        }
    }
}
