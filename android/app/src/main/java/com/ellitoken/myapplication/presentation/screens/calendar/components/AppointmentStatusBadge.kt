import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun AppointmentStatusBadge(status: String) {
    val (backgroundColor, textColor) = when (status) {
        "DOLU" -> Pair(Color(0xFFE2F6F1), Color(0xFF13A277))
        "Beklemede" -> Pair(Color(0xFFFFF9E0), Color(0xFFE6A60B))
        "Tamamlandı" -> Pair(Color(0xFFE6E6E6), Color(0xFF6B6B6B))
        "CANCEL" -> Pair(Color(0xFFFFE5E5), Color(0xFFE63946))
        else -> Pair(Color.LightGray, Color.Black)
    }

    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(backgroundColor)
            .padding(horizontal = 8.dp, vertical = 4.dp)
    ) {
        Text(
            text = if (status != "CANCEL") status else "İptal Edildi",
            color = textColor,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium
        )
    }
}