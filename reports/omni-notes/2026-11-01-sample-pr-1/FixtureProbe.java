package it.feio.android.omninotes.reviewfixture;
import java.nio.file.*;
import java.util.Collections;
import java.nio.charset.StandardCharsets;
public final class FixtureProbe {
 public static void main(String[] args) throws Exception {
  Path root=Files.createTempDirectory("review-probe");
  Path allowed=Files.createDirectory(root.resolve("notes"));
  Path outside=root.resolve("outside.txt");
  Files.write(outside,"synthetic-marker".getBytes(StandardCharsets.UTF_8));
  try {
   String result=new String(NoteExportPreview.previewSharedNote(allowed.toFile(),"../outside.txt"),StandardCharsets.UTF_8);
   if (!"synthetic-marker".equals(result)) throw new AssertionError("Traversal not reproduced");
   System.out.println("Confirmed seeded path traversal using synthetic temporary files.");
   try { NoteExportPreview.averageLength(Collections.<String>emptyList()); throw new AssertionError("Crash not reproduced"); }
   catch (ArithmeticException expected) { System.out.println("Confirmed seeded empty-list arithmetic crash."); }
  } finally { Files.delete(outside); Files.delete(allowed); Files.delete(root); }
 }
}
