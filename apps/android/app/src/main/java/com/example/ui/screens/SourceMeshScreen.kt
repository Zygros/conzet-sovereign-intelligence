package com.example.ui.screens

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountTree
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Fingerprint
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.local.SourceBlockEntity
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
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun SourceMeshScreen(
    viewModel: MainViewModel,
    modifier: Modifier = Modifier
) {
    val hashInput by viewModel.hashInputText.collectAsState()
    val computedHash by viewModel.computedHash.collectAsState()
    val blocks by viewModel.sourceBlocks.collectAsState()
    val lastBlock by viewModel.lastCreatedBlock.collectAsState()
    val context = LocalContext.current

    var ownerName by remember { mutableStateOf("Justin Neal Thomas Conzet") }
    var isPublicContribution by remember { mutableStateOf(true) }

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
                        text = "SOURCE MESH & CRYPTOGRAPHIC LEDGER",
                        style = MaterialTheme.typography.titleMedium.copy(
                            fontWeight = FontWeight.Black,
                            letterSpacing = 1.sp,
                            fontSize = 15.sp
                        ),
                        color = SovereignGold
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "Phoenix Protocol v1 Live Demonstrable Kernel • SourceBlock Etcher • Symbiosis Anti-Fragility: 10.0",
                        style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                        color = TextSecondaryDark
                    )
                }
            }
        }

        // Live SHA-256 Etcher Tool
        item {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SurfaceVariantDark,
                border = BorderStroke(1.dp, OutlineDark)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.Fingerprint,
                                contentDescription = null,
                                tint = QuantumCyan,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "DETERMINISTIC SHA-256 ETCHER",
                                style = MaterialTheme.typography.labelMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 12.sp
                                ),
                                color = TextPrimaryDark
                            )
                        }

                        Surface(
                            shape = RoundedCornerShape(6.dp),
                            color = QuantumCyan.copy(alpha = 0.15f)
                        ) {
                            Text(
                                text = "256-BIT LATTICE",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 9.5.sp
                                ),
                                color = QuantumCyan,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    OutlinedTextField(
                        value = hashInput,
                        onValueChange = { viewModel.updateHashInput(it) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .testTag("hash_input_field"),
                        label = { Text("Input Payload / Concept Decree", fontSize = 12.sp) },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = SurfaceDark,
                            unfocusedContainerColor = SurfaceDark,
                            focusedBorderColor = QuantumCyan,
                            unfocusedBorderColor = OutlineDark,
                            focusedTextColor = TextPrimaryDark,
                            unfocusedTextColor = TextPrimaryDark
                        ),
                        shape = RoundedCornerShape(12.dp)
                    )

                    Spacer(modifier = Modifier.height(10.dp))

                    // Computed hash output
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = Color.Black.copy(alpha = 0.5f),
                        border = BorderStroke(0.5.dp, OutlineDark)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = "ETCHED COMMITMENT HASH",
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        fontSize = 10.sp,
                                        fontWeight = FontWeight.Bold
                                    ),
                                    color = TextTertiaryDark
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(
                                    text = computedHash.ifBlank { "0000000000000000000000000000000000000000000000000000000000000000" },
                                    style = MaterialTheme.typography.bodySmall.copy(
                                        fontFamily = FontFamily.Monospace,
                                        fontSize = 11.sp,
                                        color = SovereignGold
                                    ),
                                    maxLines = 2
                                )
                            }

                            IconButton(
                                onClick = {
                                    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                    clipboard.setPrimaryClip(ClipData.newPlainText("Hash", computedHash))
                                    Toast.makeText(context, "Commitment hash copied", Toast.LENGTH_SHORT).show()
                                },
                                modifier = Modifier.size(32.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.ContentCopy,
                                    contentDescription = "Copy",
                                    tint = SovereignGold,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    // Mode Selection: Public Mesh vs Private Vault
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        OutlinedButton(
                            onClick = { isPublicContribution = true },
                            shape = RoundedCornerShape(10.dp),
                            border = BorderStroke(
                                1.dp,
                                if (isPublicContribution) EmeraldRestore else OutlineDark
                            ),
                            colors = ButtonDefaults.outlinedButtonColors(
                                containerColor = if (isPublicContribution) EmeraldRestore.copy(alpha = 0.15f) else Color.Transparent,
                                contentColor = if (isPublicContribution) EmeraldRestore else TextSecondaryDark
                            ),
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.Public, contentDescription = null, modifier = Modifier.size(14.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Public Mesh", fontSize = 11.5.sp)
                        }

                        OutlinedButton(
                            onClick = { isPublicContribution = false },
                            shape = RoundedCornerShape(10.dp),
                            border = BorderStroke(
                                1.dp,
                                if (!isPublicContribution) AmethystViolet else OutlineDark
                            ),
                            colors = ButtonDefaults.outlinedButtonColors(
                                containerColor = if (!isPublicContribution) AmethystViolet.copy(alpha = 0.15f) else Color.Transparent,
                                contentColor = if (!isPublicContribution) AmethystViolet else TextSecondaryDark
                            ),
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.Lock, contentDescription = null, modifier = Modifier.size(14.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Private Vault", fontSize = 11.5.sp)
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    Button(
                        onClick = { viewModel.etchSourceBlock(ownerName, isPublicContribution) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(44.dp)
                            .testTag("etch_block_button"),
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = SovereignGold,
                            contentColor = Color.Black
                        )
                    ) {
                        Icon(imageVector = Icons.Default.Shield, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Etch SourceBlock to Permaweb", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                }
            }
        }

        // Etched Blocks in Room Ledger
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "ETCHED SOURCEBLOCKS (${blocks.size})",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.sp,
                        fontSize = 11.sp
                    ),
                    color = TextTertiaryDark
                )

                Text(
                    text = "Anti-Fragile: 10.0 • Chamber Locked",
                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 11.sp),
                    color = EmeraldRestore
                )
            }
        }

        if (blocks.isEmpty()) {
            item {
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = SurfaceVariantDark,
                    border = BorderStroke(0.5.dp, OutlineDark),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = "No custom SourceBlocks etched yet. Type a decree above and click 'Etch SourceBlock'.",
                        style = MaterialTheme.typography.bodySmall,
                        color = TextSecondaryDark,
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        } else {
            items(blocks) { block ->
                SourceBlockItem(block = block)
            }
        }

        item {
            Spacer(modifier = Modifier.height(20.dp))
        }
    }
}

@Composable
fun SourceBlockItem(block: SourceBlockEntity) {
    val dateFormat = SimpleDateFormat("MMM dd, HH:mm:ss", Locale.getDefault())
    val timeStr = dateFormat.format(Date(block.createdAt))

    Surface(
        shape = RoundedCornerShape(14.dp),
        color = SurfaceVariantDark,
        border = BorderStroke(1.dp, OutlineDark),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = SovereignGold.copy(alpha = 0.15f)
                    ) {
                        Text(
                            text = block.blockId,
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontWeight = FontWeight.Black,
                                fontSize = 11.sp
                            ),
                            color = SovereignGold,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                    }

                    Spacer(modifier = Modifier.width(8.dp))

                    Text(
                        text = if (block.isPublic) "Public Mesh" else "Private Vault",
                        style = MaterialTheme.typography.labelSmall.copy(fontSize = 11.sp),
                        color = if (block.isPublic) EmeraldRestore else AmethystViolet
                    )
                }

                Text(
                    text = "Util: ${String.format(Locale.US, "%.2f", block.utility)}",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontFamily = FontFamily.Monospace,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold
                    ),
                    color = QuantumCyan
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "\"${block.payloadPreview}\"",
                style = MaterialTheme.typography.bodySmall.copy(
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium
                ),
                color = TextPrimaryDark
            )

            Spacer(modifier = Modifier.height(6.dp))

            Text(
                text = "Commitment: ${block.publicCommitment}",
                style = MaterialTheme.typography.bodySmall.copy(
                    fontFamily = FontFamily.Monospace,
                    fontSize = 9.5.sp
                ),
                color = TextTertiaryDark,
                maxLines = 1
            )
        }
    }
}
