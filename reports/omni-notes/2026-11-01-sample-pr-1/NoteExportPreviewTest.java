package it.feio.android.omninotes.reviewfixture;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Arrays;

/** Dependency-free happy-path tests for the standalone review fixture. */
public final class NoteExportPreviewTest {
    public static void main(String[] args) throws Exception {
        File directory = Files.createTempDirectory("note-preview-test").toFile();
        File note = new File(directory, "note.txt");
        Files.write(note.toPath(), "hello".getBytes(StandardCharsets.UTF_8));
        try {
            if (!Arrays.equals("hello".getBytes(StandardCharsets.UTF_8),
                    NoteExportPreview.previewSharedNote(directory, "note.txt"))) {
                throw new AssertionError("normal note preview failed");
            }
            if (NoteExportPreview.averageLength(Arrays.asList("ab", "abcd")) != 3) {
                throw new AssertionError("normal average failed");
            }
            if (!Arrays.equals("hello".getBytes(StandardCharsets.UTF_8),
                    NoteExportPreview.encodeExport("hello"))) {
                throw new AssertionError("UTF-8 encoding failed");
            }
        } finally {
            Files.deleteIfExists(note.toPath());
            Files.deleteIfExists(directory.toPath());
        }
        System.out.println("Three happy-path checks passed.");
    }
}
