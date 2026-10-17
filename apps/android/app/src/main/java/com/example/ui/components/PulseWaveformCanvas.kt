package com.example.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import com.example.ui.theme.QuantumCyan
import com.example.ui.theme.SovereignGold
import kotlin.math.sin

@Composable
fun PulseWaveformCanvas(
    modifier: Modifier = Modifier,
    isPulsing: Boolean = true,
    primaryColor: Color = SovereignGold,
    secondaryColor: Color = QuantumCyan
) {
    val infiniteTransition = rememberInfiniteTransition(label = "pulse_transition")
    val phase by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = if (isPulsing) (2 * Math.PI.toFloat()) else 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(2400, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "phase"
    )

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(72.dp)
    ) {
        val width = size.width
        val height = size.height
        val midY = height / 2f

        // Draw background grid lines
        val gridColor = Color.White.copy(alpha = 0.05f)
        for (i in 0..4) {
            val y = height * (i / 4f)
            drawLine(
                color = gridColor,
                start = Offset(0f, y),
                end = Offset(width, y),
                strokeWidth = 1f
            )
        }

        // Generate dynamic wave 1 (Primary Gold Wave)
        val path1 = Path()
        val path2 = Path()

        val points = 80
        for (i in 0..points) {
            val x = (i / points.toFloat()) * width
            val normalizedX = (i / points.toFloat()) * 4f * Math.PI.toFloat()
            val envelope = (sin(i / points.toFloat() * Math.PI).toFloat()) // Windowing function

            val y1 = midY + (sin(normalizedX - phase) * 22f * envelope)
            val y2 = midY + (sin(normalizedX * 1.5f + phase * 0.8f) * 14f * envelope)

            if (i == 0) {
                path1.moveTo(x, y1)
                path2.moveTo(x, y2)
            } else {
                path1.lineTo(x, y1)
                path2.lineTo(x, y2)
            }
        }

        // Draw secondary cyan wave glow
        drawPath(
            path = path2,
            brush = Brush.horizontalGradient(
                colors = listOf(
                    secondaryColor.copy(alpha = 0.2f),
                    secondaryColor.copy(alpha = 0.8f),
                    secondaryColor.copy(alpha = 0.2f)
                )
            ),
            style = Stroke(width = 2.dp.toPx())
        )

        // Draw primary gold wave
        drawPath(
            path = path1,
            brush = Brush.horizontalGradient(
                colors = listOf(
                    primaryColor.copy(alpha = 0.3f),
                    primaryColor,
                    primaryColor.copy(alpha = 0.3f)
                )
            ),
            style = Stroke(width = 3.dp.toPx())
        )

        // Draw center pulse spark
        val sparkX = (phase / (2 * Math.PI.toFloat())) * width
        val sparkEnvelope = sin((sparkX / width) * Math.PI).toFloat()
        val sparkY = midY + (sin((sparkX / width) * 4f * Math.PI.toFloat() - phase) * 22f * sparkEnvelope)

        drawCircle(
            color = Color.White,
            radius = 4.dp.toPx(),
            center = Offset(sparkX, sparkY)
        )
        drawCircle(
            color = primaryColor.copy(alpha = 0.4f),
            radius = 10.dp.toPx(),
            center = Offset(sparkX, sparkY)
        )
    }
}
