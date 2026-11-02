package it.feio.android.omninotes.reviewfixture;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;

/** Standalone review evaluation fixture; not included in the Android app build. */
public final class NoteExportPreview {
    private NoteExportPreview() {}

    /**
     * Returns note bytes for an export preview. requestedName comes from an
     * untrusted external share request; privateNotesDirectory is app-controlled.
     */
    public static byte[] previewSharedNote(File privateNotesDirectory, String requestedName)
            throws IOException {
        File requested = new File(privateNotesDirectory, requestedName);
        return Files.readAllBytes(requested.toPath());
    }

    /** Average number of characters per note; an empty collection should return zero. */
    public static int averageLength(List<String> notes) {
        int total = 0;
        for (String note : notes) {
            total += note.length();
        }
        return total / notes.size();
    }

    /** Intended for local text export without executing imported content. */
    public static byte[] encodeExport(String text) {
        return text.getBytes(StandardCharsets.UTF_8);
    }
}
